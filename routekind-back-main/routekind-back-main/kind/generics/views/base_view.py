from typing import TYPE_CHECKING, List, cast
from functools import wraps

from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError, APIException
from rest_framework.request import HttpRequest
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from django.db.models import QuerySet
from django.db import transaction
from django.shortcuts import get_object_or_404 as _get_object_or_404

from kind.connections.models.api_connection_model import ApiConnectionModuleWebhookResponse, WebhookValidationError
from kind.generics.models.base_model import GenericBaseModel
from kind.generics.paginations.optional_pagination import OptionalPagination
from kind.generics.serializers.base_seriaizer import _get_connection_module

if TYPE_CHECKING:
    from kind.customauth.models import User
    from kind.connections.models import ApiConnectionModule, ApiConnectionModuleWebhook


def get_object_or_404(queryset, *filter_args, **filter_kwargs):
    """
    Same as Django's standard shortcut, but make sure to also raise 404
    if the filter_kwargs don't match the required types.
    """
    try:
        return _get_object_or_404(queryset, *filter_args, **filter_kwargs)
    except (TypeError, ValueError, ValidationError):
        raise Http404


def webhook_sender_handler(func):
    @wraps(func)
    def wrapper(view: 'GenericConnectionMixin', request: HttpRequest, *args, **kwargs):
        try:
            with transaction.atomic():
                result = func(view, request, *args, **kwargs)
                # ! No se puede manejar validate_connection_operation aquí porque un mismo request podría involucrar a varios módulos, y de esta forma solo se alcanza al módulo padre
                # if hasattr(view, 'is_valid_connection_module') and view.is_valid_connection_module():
                #     # Validate that the operation made throught an api connection in valid
                #     view.validate_connection_operation(request)
                if hasattr(view, 'send_webhooks') and view.connection_action:
                    # Invoke operation webhooks (while not maded througth an api connection)
                    view.send_webhooks(request, result.data, view.connection_action)

                return result
        except WebhookValidationError as webhook_error:
            error_details: List[dict] = webhook_error.args[0].get("error").get("details")
            for error_detail in error_details:
                error: dict = list(error_detail.values())[0]
                ApiConnectionModuleWebhookResponse.objects.create(
                    webhook_id=error.get("webhook"),
                    input_data=error.get("input_data"),
                    response_error=error.get("response_error"),
                    company=request.user.company
                )
            return Response(webhook_error.args[0], status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            raise ex

    return wrapper


class GenericConnectionMixin:
    connection_module: "ApiConnectionModule"
    operation_instance: "GenericBaseModel"
    connection_action: str

    def _get_model_class(self):
        serializer_class = self.get_serializer_class()
        return serializer_class.Meta.model

    def is_valid_connection_module(self, *, raise_exception=False):
        model = self.serializer_class.Meta.model
        request = self.request
        self.connection_module = _get_connection_module(model, request, raise_exception=raise_exception)
        return self.connection_module is not None

    def send_webhooks(self, request: HttpRequest, data: dict, action: str):
        # SEND EXISTING WEBHOOKS
        user: 'User' = request.user
        webhooks = user.company.get_api_connection_webhooks_by_model(
            self._get_model_class(),
            on_action=action
        )
        webhook_data = data
        webhook_errors = []
        webhooks_responses = {}
        for webhook in webhooks.all():
            webhook: 'ApiConnectionModuleWebhook'
            try:
                processed_webhook_data = webhook.connection_module.process_output_data(webhook_data)
                webhook_response, is_success = webhook.send_wekhook(processed_webhook_data)
                webhooks_responses[webhook.name] = webhook_response
                if is_success and webhook.create_response_clinet_id_field_name:
                    # Extract client_id
                    field_paths = webhook.create_response_clinet_id_field_name.split(".")
                    clinet_id = {**webhook_response}
                    for field_path in field_paths:
                        clinet_id = clinet_id.get(field_path, None)
                        if clinet_id is None:
                            break

                    # Check client id exists
                    if not clinet_id:
                        raise ValidationError({
                            webhook.create_response_clinet_id_field_name:
                                "This field is not defined in webhook response, "
                                "but is required to set clinet_id value."
                        })

                    # Never should happend
                    if not self.operation_instance:
                        raise APIException({'error': "'operation_instance' is not defined."})

                    # Put new key
                    webhook.connection_module.put_key(str(self.operation_instance.id), clinet_id)
            except WebhookValidationError as ex:
                webhook_errors.append({webhook.name: ex.args[0]})

        if len(webhook_errors) > 0:
            raise WebhookValidationError({
                "error": {
                    "message": f"{len(webhook_errors)} webhooks failed.",
                    "details": webhook_errors
                }
            })

        # TODO: Save 'webhooks_responses' into additional_information.created_webhooks_response
        self.webhooks_responses = webhooks_responses

    def validate_connection_operation(self, request: HttpRequest):
        raise APIException("'validate_connection_operation' is not implemented yet.")


class ConnectionDetailMixin(GenericConnectionMixin):

    def _get_object_by_connection_client_id(self):
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        clinet_id = self.kwargs[lookup_url_kwarg]
        self.kwargs[lookup_url_kwarg] = self.connection_module.get_local_id_from_client_id(clinet_id)

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def get_object(self):
        if not self.is_valid_connection_module(raise_exception=True):
            return super().get_object()

        return self._get_object_by_connection_client_id()


class ConnectionCreateMixin(GenericConnectionMixin):
    connection_action = 'create'

    def perform_create(self, serializer):
        self.operation_instance = serializer.save()

    def validate_connection_operation(self, request: HttpRequest):
        request_data: dict = request.data
        client_id = request_data.get('client_id')

        # Validate clientId exists
        if (not client_id):
            raise ValidationError({"clientId": "This field is required."})

        # Register clientId to connection
        # TODO: Remover key cuando se elimina el registro
        self.connection_module.put_key(
            str(self.operation_instance.id),
            request_data.get("client_id")
        )

    @transaction.non_atomic_requests
    @webhook_sender_handler
    def create(self, request: HttpRequest, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class ConnectionUpdateMixin(GenericConnectionMixin):
    connection_action = 'update'

    def perform_update(self, serializer):
        self.operation_instance = serializer.save()

    def validate_connection_operation(self, request: HttpRequest):
        pass

    @transaction.non_atomic_requests
    @webhook_sender_handler
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class BaseModelViewSet(
    ConnectionCreateMixin,
    ConnectionUpdateMixin,
    ConnectionDetailMixin,
    ModelViewSet,
):
    class CustomPermission(IsAuthenticated):

        def __init__(self, app_name: str, action: str) -> None:
            self.app_name = app_name
            self.action = action
            super().__init__()

        def has_permission(self, request: HttpRequest, view):
            user: 'User' = request.user

            if user.is_superuser:
                return True

            if not hasattr(user, "has_permission"):
                return False

            return (
                user.has_permission(f'{self.app_name}.{self.action}') or
                user.has_permission(f'{self.app_name}.all')
            )

    pagination_class = OptionalPagination

    def get_model_class(self):
        return cast(GenericBaseModel, self.get_serializer_class().Meta.model)

    def get_app_name(self):
        model_class = self.get_model_class()
        # Get custom app name
        custom_app_name = getattr(model_class, 'app_name', None)
        if custom_app_name is not None:
            return custom_app_name
        # Return default app name
        return self.get_model_class()._meta.app_label

    def get_permission_action(self):
        return getattr(self, 'custom_action', None) or (
            'list' if self.action == 'retrieve' else
            'update' if self.action == 'partial_update' else
            self.action
        )

    def get_queryset(self) -> QuerySet:
        user: User = self.request.user

        # Get base queryset
        try:
            qs = cast(QuerySet, super().get_queryset())
        except:
            qs = self.get_model_class().objects.all()

        # Filter registers by user's company
        qs = qs.filter(company=user.company)

        # Filter by permission
        app_name = self.get_app_name()
        action = self.get_permission_action()
        required_permission = f"{app_name}.{action}"
        if (
            not user.has_permission(required_permission, exact=True) and
            user.has_permission(f'{required_permission}-own', exact=True)
        ):
            try:
                qs = qs.filter(users__id=user.id)
            except:
                pass

        # Return filtered queryset
        return qs

    def get_permissions(self):
        # Use default permissions
        if (
            getattr(self, 'use_default_permissions', False) and
            self.use_default_permissions
        ):
            return super().get_permissions()

        # Use custom permissions
        app_name = self.get_app_name()
        action = self.get_permission_action()
        return [
            BaseModelViewSet.CustomPermission(
                app_name=app_name,
                action=action
            )
        ]
