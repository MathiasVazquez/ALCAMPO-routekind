from typing import TYPE_CHECKING

from django.contrib.contenttypes.models import ContentType
from rest_framework.request import HttpRequest
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from .nested_model_serializer_mixin import NestedModelSerializerMixin

if TYPE_CHECKING:
    from kind.customauth.models import User, AuthToken
    from kind.connections.models import ApiConnectionModule


def _get_connection_module(model, request: HttpRequest, *, raise_exception=False):
    user: 'User' = request.user

    # Check this is an connection api request token
    if not user or not user.is_connection_request(request):
        return None

    # Get used request token
    auth_token: 'AuthToken' = user.jwt_auth_tokens.filter(type="api").first()
    if not auth_token:
        return None

    content_type = ContentType.objects.get_for_model(model, for_concrete_model=True)
    module: 'ApiConnectionModule' = auth_token.connection.modules.filter(content_type=content_type).first()
    if not module and raise_exception:
        raise ValidationError({"error": f"Module '{str(content_type)}' not defined for this connection."})
    return module


class BaseSerializer(NestedModelSerializerMixin):
    def get_user(self) -> 'User':
        request: HttpRequest = self.context.get('request', None)
        if not request:
            return None
        user: 'User' = request.user
        return user

    def _is_valid_connection_module(self, *, raise_exception=False):
        model = self.__class__.Meta.model
        request = self.context.get('request')
        self.connection_module = _get_connection_module(model, request, raise_exception=raise_exception)
        return self.connection_module is not None

    def _get_client_id(self):
        request_data = self.context.get('request').data
        client_id = self.context.get('data', request_data).get("client_id", None)
        return client_id

    def get_object(self):
        data = self.context.get(
            "data",
            self.context.get("request").data
        )
        return self.get_instance_by_unique_identifiers(
            model_class=self.Meta.model,
            data=data
        )

    def create(self, validated_data: dict):

        # Check if the instance already exists and update
        existing_instance = self.get_object()
        if existing_instance:
            return self.update(existing_instance, validated_data)

        # Create a new instance
        instance = super().create(validated_data)

        # Put client id on create a new register via connection token
        if self._is_valid_connection_module():
            client_id = self._get_client_id()
            if not client_id:
                raise serializers.ValidationError({"client_id": "This field is required."})
            self.connection_module.put_key(str(instance.id), client_id)

        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)

        # Put client id on create a new register via connection token
        if self._is_valid_connection_module():
            client_id = self._get_client_id()
            if client_id:
                local_id = str(instance.id)
                if not self.connection_module.exists_key_value(local_id, client_id):
                    self.connection_module.put_key(local_id, client_id)

        return instance

    def to_internal_value(self, data):
        if self._is_valid_connection_module(raise_exception=True):
            data = self.connection_module.process_input_data(data)
        return super().to_internal_value(data)

    def to_representation(self, instance):
        data = super().to_representation(instance)

        if self._is_valid_connection_module(raise_exception=True):
            data["clientId"] = self.connection_module.client_id_keys.get(str(instance.id), None)
            return self.connection_module.process_output_data(data)

        # if hasattr(self, "webhooks_responses") and self.webhooks_responses:
        #     data["$webhooksResponses"] = self.webhooks_responses

        return data

    @property
    def ip_address(self):
        request: 'HttpRequest' = self.context.get("request")
        return request.META.get('REMOTE_ADDR')

    @property
    def device_name(self):
        request: 'HttpRequest' = self.context.get("request")
        return request.headers.get("Device", None)
