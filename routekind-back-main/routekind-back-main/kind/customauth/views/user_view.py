from typing import TYPE_CHECKING

from django.db.models import QuerySet
from django.http import HttpRequest
from rest_framework import status
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from kind.customauth.serializers import UserSerializer
from kind.customauth.utils.crypt import decrypt_password
from kind.generics.views.base_view import BaseModelViewSet
from kind.customauth.auths import is_valid_recaptcha
from kind.customauth.models import User
from kind.useraudit.models.user_audit_model import UserAudit

if TYPE_CHECKING:
    from kind.customauth.models import UserRole


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=4)
    confirm_password = serializers.CharField(min_length=4)
    token = serializers.CharField()

    def validate_password(self, value: str):
        if value != self.initial_data.get('confirm_password'):
            raise ValidationError("Las contraseñas no coinciden")

    def validate_confirm_password(self, value: str):
        if value != self.initial_data.get('password'):
            raise ValidationError("Las contraseñas no coinciden")


class UserView(BaseModelViewSet):
    serializer_class = UserSerializer
    # permission_classes = [IsAdminUser]

    def get_queryset(self) -> QuerySet:
        user: User = self.request.user
        qs = super().get_queryset()
        qs = user.filter_users_by_restricted_roles(qs)
        return qs

    # def create(self, request: HttpRequest, *args, **kwargs):
    #     try:
    #         return super().create(request, *args, **kwargs)
    #     except Exception as ex:
    #         return Response(ex.args, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def reset_password(self, request: HttpRequest, pk: str = None):
        password = decrypt_password(request.data.get("password"))
        confirm_password = decrypt_password(request.data.get("confirm_password"))

        data: dict = {
            "id": request.data.get("id"),
            "password": password,
            "confirm_password": confirm_password,
            "token": request.data.get("token"),
        }

        # Validate input data
        serializer = ResetPasswordSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        # Validate recaptcha token
        recaptcha_token = data.get('token')
        is_valid_recaptcha(recaptcha_token, raise_exception=True)

        # Set new temporal password
        user: 'User' = self.get_object()
        # if user.current_temporal_password is not None:
        #     logs.append(f'Existe una solicitud pendiente en estado {user.current_temporal_password.status}')
        #     user.current_temporal_password.complete(password)
        # else:
        #     logs.append(f'No existe una solicitud pendiente')
        #     logs.append(f'La cantidad total de solicitudes son {user.temporal_password_records.count()}')
        user.create_temporal_password_request().approve(password, request.user)

        # Audit
        ip_address = request.META.get('REMOTE_ADDR')
        device_name = request.headers.get("Device", None)
        UserAudit.add_users_log(
            user,
            request.user,
            ip_address,
            device_name,
            entry_log=f'{request.user.name} (@{request.user.username}) ha cambiado la contraseña del usuario "{user.name} (@{user.username})".'
        )

        return Response()

    @action(detail=True, methods=['post'])
    def confirm_admin_password_request(self, request: HttpRequest, pk: str = None):
        password = decrypt_password(request.data.get("password"))
        confirm_password = decrypt_password(request.data.get("confirm_password"))

        data: dict = {
            "password": password,
            "confirm_password": confirm_password,
            "token": request.data.get("token"),
        }

        # Validate input data
        serializer = ResetPasswordSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        # Validate recaptcha token
        recaptcha_token = data.get('token')
        is_valid_recaptcha(recaptcha_token, raise_exception=True)

        # Set new temporal password
        detailed_user: 'User' = self.get_object()
        detailed_user.set_temporal_password(data.get('password'), setted_by=request.user)

        return Response()


class UserProfileView(APIView):
    allowed_self_update_props = ['coords']

    def get(self, request: HttpRequest):
        data = UserSerializer(request.user, context={"request": request}).data
        return Response(data)

    def patch(self, request: HttpRequest):
        validated_data = {
            key: request.data[key]
            for key in self.allowed_self_update_props
            if key in request.data
        }
        context = {"request": request}
        update_serializer = UserSerializer(
            instance=request.user,
            data=validated_data,
            partial=True,
            context=context
        )
        update_serializer.is_valid(raise_exception=True)
        update_serializer.save()
        request.user.save()

        get_serializer = UserSerializer(request.user, context=context)
        return Response(get_serializer.data)


class ResetUserPasswordView(APIView):

    def post(self, request: HttpRequest):
        password = decrypt_password(request.data.get("password"))
        confirm_password = decrypt_password(request.data.get("confirm_password"))

        data: dict = {
            "password": password,
            "confirm_password": confirm_password,
            "token": request.data.get("token"),
        }
        user: 'User' = request.user

        # Validate request data
        context = {"request": request}
        serializer = ResetPasswordSerializer(data=data, context=context)
        serializer.is_valid(raise_exception=True)

        # Validate recaptcha token
        recaptcha_token = data.get('token')
        is_valid_recaptcha(recaptcha_token, raise_exception=True)

        # Validate new temporal password
        # if user.current_temporal_password is not None and user.current_temporal_password.status == 'pending':
        #     raise ValidationError({"error": "Ya existe una solicitud pendiente."})

        # Create a new TemporalPassword instance and approve it
        password = data.get('password')
        if user.current_temporal_password is not None:
            user.current_temporal_password.complete(password)
        # user.create_temporal_password_request().approve(password, user)

        # Set new passwrod
        user.require_change_password_at_first_login_completed = True
        user.set_valid_password(password)
        user.save()

        # Audit
        ip_address = request.META.get('REMOTE_ADDR')
        device_name = request.headers.get("Device", None)
        UserAudit.add_users_log(
            user,
            request.user,
            ip_address,
            device_name,
            entry_log=f'{request.user.name} (@{request.user.username}) ha cambiado su contraseña.'
        )

        return Response()


class RequestAdminNewPassword(APIView):
    permission_classes = (AllowAny,)

    def post(self, request: HttpRequest):
        data: dict = request.data

        # Validate username
        username = data.get("username")
        user_filter = User.objects.filter(username=username)
        if not user_filter.exists():
            # raise ValidationError({"username": "El nombre de usuario ingresado no es válido."})
            return Response()
        user: 'User' = user_filter.first()

        # Validate recaptcha token
        recaptcha_token = data.get('token')
        is_valid_recaptcha(recaptcha_token, raise_exception=True)

        # Validate new temporal password
        if user.current_temporal_password is not None and user.current_temporal_password.status == 'pending':
            return Response()
            # raise ValidationError({"error": "Ya existe una solicitud pendiente."})

        # Create a new TemporalPassword instance
        user.create_temporal_password_request()

        # Set new status
        user.require_change_password_at_first_login_completed = False
        user.save()

        return Response()
