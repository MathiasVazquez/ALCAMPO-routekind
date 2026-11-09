import secrets
import hashlib
import base64
import requests
import json
import uuid

from typing import TYPE_CHECKING

from django.db import models
from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from django.contrib.contenttypes.fields import Generic

from kind.customauth.models.auth_token_model import AUTH_TOKEN_API
from kind.generics.models.base_model import CustomModelAbstract
from kind.generics.models.named_model import StrictNamedModelMixin
from kind.connections.utils.crypt import vigenere_encrypt, vigenere_decrypt
from kind.customauth.models import User, AuthToken
from kind.generics.utils import eval_contextualized_js_code

if TYPE_CHECKING:
    from kind.companies.models import Company


WEBHOOK_METHDOS_CHOICES = (
    ("post", "POST"),
    ("patch", "PATCH"),
    ("put", "PUT"),
    ("delete", "DELETE"),
)

WEBHOOK_ACTIONS_CHOICES = (
    ("create", "CREATE"),
    ("update", "UPDATE"),
    ("delete", "DELETE"),
)

WEBHOOK_ON_ERROR_CHOICES = (
    ("skip", "SKIP"),
    ("raise", "RAISE"),
    # ("delete", "DELETE"),
)


class WebhookValidationError(ValidationError):
    def __init__(self, detail=None, code=None):
        super().__init__(detail, code)


class ApiConnectionModuleWebhookResponse(CustomModelAbstract):
    input_data = models.JSONField(default=None, null=True, blank=True)
    response_data = models.JSONField(default=None, null=True, blank=True)
    response_error = models.JSONField(default=None, null=True, blank=True)
    webhook: 'ApiConnectionModuleWebhook' = models.ForeignKey(
        'ApiConnectionModuleWebhook',
        related_name="responses",
        on_delete=models.CASCADE,
    )
    # TODO: Save webhook state (method, url, params, headers) to implement 'retry' method

    @property
    def is_error(self):
        return bool(self.response_error)


class ApiConnectionModuleWebhook(CustomModelAbstract, StrictNamedModelMixin):
    on_action = models.CharField(max_length=8, choices=WEBHOOK_ACTIONS_CHOICES)
    on_error = models.CharField(max_length=8, default="skip", choices=WEBHOOK_ON_ERROR_CHOICES)

    method = models.CharField(max_length=8, choices=WEBHOOK_METHDOS_CHOICES)
    headers = models.JSONField(default=None, null=True, blank=True)
    params = models.JSONField(default=None, null=True, blank=True)
    url = models.CharField(max_length=2040)
    connection_module: 'ApiConnectionModule' = models.ForeignKey(
        'ApiConnectionModule',
        related_name='webhooks',
        on_delete=models.CASCADE
    )
    create_response_clinet_id_field_name = models.CharField(max_length=32, blank=True, default="")
    responses: models.Manager

    def send_wekhook(self, data):
        def uuid_serializer(obj):
            if isinstance(obj, uuid.UUID):
                return str(obj)
            raise TypeError("Tipo no serializable")

        try:
            # with transaction.atomic():
            methdo_fn = getattr(requests, self.method)
            response = methdo_fn(
                url=self.url,
                data=json.dumps(data, default=uuid_serializer),
                params=self.params,
                headers=self.headers,
            )
            if response.status_code >= 400:
                raise ValidationError({
                    "code": response.status_code,
                    "content": str(response.content),
                })
            response_json = response.json()

            ApiConnectionModuleWebhookResponse.objects.create(
                webhook=self,
                input_data=data,
                response_data=response_json,
                company=self.company
            )

            return response_json, True
        except Exception as ex:
            _err = {"error": ex.args[0]}

            if self.on_error == 'skip':
                return _err, False

            raise WebhookValidationError({
                "webhook": str(self.id),
                "input_data": data,
                "response_error": _err
            }) from ex


class ApiConnectionModule(CustomModelAbstract):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    client_id_keys = models.JSONField(default=dict, blank=True)
    connection: 'ApiConnection' = models.ForeignKey(
        'ApiConnection',
        related_name='modules',
        on_delete=models.CASCADE,
    )
    output_processor_code = models.TextField(default='', blank=True)
    input_processor_code = models.TextField(default='', blank=True)
    webhooks: models.Manager

    def process_output_data(self, data):
        code: str = self.output_processor_code
        if not code:
            return data
        if type(data) == list:
            code = f"return data.map(data => {{ code }});"
        return eval_contextualized_js_code(code, data)

    def process_input_data(self, data):
        code: str = self.input_processor_code
        if not code:
            return data
        if type(data) == list:
            code = f"return data.map(data => {{ code }});"
        return eval_contextualized_js_code(code, data)

    # connection_user = models.OneToOneField(
    #     'customauth.User',
    #     related_name="connection",
    #     on_delete=models.CASCADE,
    # )
    def get_local_id_from_client_id(self, client_id: str):
        for key, val in self.client_id_keys.items():
            if val == client_id:
                return key
        return None

    def put_key(self, local_id: str, client_id: str):
        # Validate client_id is unique
        self.client_id_keys: dict
        if client_id in self.client_id_keys.values():
            prev_local_id: str = self.get_local_id_from_client_id(client_id)

            # Is putting the same
            if prev_local_id == local_id:
                return

            # Validate prev_local_id instance exists
            if not self.exists_instance_by_local_id(prev_local_id):
                prev_local_id = None

            # Already exists
            if prev_local_id is not None:
                raise ValidationError(
                    {"clientId": f"This field must be unique, but {client_id} is a duplicate."}
                )

        # Set client_id and save
        self.client_id_keys[local_id] = client_id
        self.save()

    def exists_key_value(self, local_id: str, client_id: str):
        return self.client_id_keys[local_id] == client_id

    def exists_instance_by_local_id(self, local_id: str):
        # Get instance from content_type (model)
        model_class = self.content_type.model_class()
        return model_class.objects.filter(id=local_id).exists()

    def get_instance_by_client_id(self, client_id: str):
        # Get local id
        local_id: str = self.get_local_id_from_client_id(client_id)

        # Validate local_id exists
        if local_id is None:
            raise ValidationError(
                {'error': f'There is not a defined id for client_id {client_id}.'}
            )

        # Get instance from content_type (model)
        model_class = self.content_type.model_class()
        return model_class.objects.filter(id=local_id).first()

    def __str__(self) -> str:
        return f"{str(self.content_type)}"


class ApiConnection(CustomModelAbstract, StrictNamedModelMixin):
    label = models.CharField(max_length=510)
    api_key = models.CharField(max_length=256, blank=True, default='')
    # is_something = models.CharField(max_length=256, blank=True, default='')
    # api_key_salt = models.CharField(max_length=256, blank=True, default='')
    api_key_secret = models.CharField(max_length=300, blank=True, default='')
    modules: models.Manager
    # connection_user_auth: 'User' = models.OneToOneField(
    #     'customauth.User',
    #     null=True,
    #     blank=True,
    #     related_name='connection',
    #     on_delete=models.CASCADE
    # )
    auth_token: 'AuthToken' = models.OneToOneField(
        AuthToken,
        null=True,
        blank=True,
        related_name='connection',
        on_delete=models.CASCADE
    )

    company: 'Company' = models.ForeignKey(
        'companies.Company',
        null=True,
        related_name='api_connections',
        on_delete=models.PROTECT,
    )

    def get_module(self, model_class) -> 'ApiConnectionModule':
        content_type = ContentType.objects.get_for_model(model_class)
        return self.modules.filter(content_type=content_type).first()

    def regenerate_api_keys(self, *, save=True):
        # Validate user is admin
        if not self.created_by.is_admin:
            raise ValidationError({"error": "User must be admin to create an API token"})

        # Delete previos token
        if self.auth_token:
            self.auth_token.delete()

        # Create a new token
        refresh_token = TokenObtainPairSerializer.get_token(self.created_by)
        refresh = str(refresh_token)
        access = str(refresh_token.access_token)

        # Register token
        token = AuthToken.objects.create(
            user=self.created_by,
            access=access,
            refresh=refresh,
            company=self.created_by.company,
            type=AUTH_TOKEN_API
        )
        self.auth_token = token

        # Save tokens
        self.api_key_secret = access  # hashlib.sha256(secrets.token_urlsafe(64).encode()).hexdigest()
        self.api_key = vigenere_encrypt(str(self.id), self.api_key_secret)

        if save:
            self.save()

    def on_update(self):
        # Regenerate keys
        self.regenerate_api_keys(save=False)

    def save(self, *args, **kwargs):
        self.on_update()
        result = super().save(*args, **kwargs)
        return result

    def __str__(self) -> str:
        return self.label
