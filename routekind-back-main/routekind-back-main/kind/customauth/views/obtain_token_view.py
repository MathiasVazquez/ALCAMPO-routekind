from django.db import transaction
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from django.utils.translation import gettext_lazy as _

from kind.customauth.models import AuthToken
from kind.customauth.models.auth_token_model import AUTH_TOKEN_ACCESS
from kind.customauth.auths import is_valid_recaptcha
from kind.customauth.models import User
from kind.customauth.utils.crypt import decrypt_password

# if TYPE_CHECKING:


RECAPTCH_HOST = "https://www.google.com/recaptcha/api/siteverify"
RECAPTCH_SECRET = "6Le3ur4pAAAAAGlTWstd1A_hH-n9XH2csSdzN9jS"


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    token = serializers.CharField()

    default_error_messages = {
        # "no_active_account": _("No active account found with the given credentials")
        "no_active_account": "No se encontró una cuenta activa con las credenciales dadas",
        "blocked_account": "La cuenta se encuentra temporalmente bloqueada, vuelva a intentarlo más tarde"
    }

    def validate(self, attrs: dict):
        password = decrypt_password(attrs.get("password"))

        attrs: dict = {
            "password": password,
            "username": attrs.get("username"),
            "token": attrs.get("token"),
        }

        # Generate access
        data = super().validate(attrs)

        #
        # USER VALIDATED: PASSWORD IS CORRECT
        #

        access = data["access"]

        # Get user
        user: 'User' = self.user

        # Validate blocked
        if user.is_blocked:
            raise AuthenticationFailed(
                self.default_error_messages["blocked_account"],
                "no_active_account",
            )

        # Remove prev user token
        AuthToken.objects.filter(
            user=user,
            type=AUTH_TOKEN_ACCESS,
        ).delete()

        # Save token in database
        AuthToken.objects.create(
            user=user,
            access=access,
            refresh=data["refresh"],
            company=user.company,
            type=AUTH_TOKEN_ACCESS,
        )

        # Validate recaptcha token
        recaptcha_token = attrs.get('token')
        is_valid_recaptcha(recaptcha_token, raise_exception=True)

        # Validate temporal password
        if (
            user.current_temporal_password is not None and
            user.current_temporal_password.has_expired
        ):
            raise ValidationError({
                'error': 'Contraseña expirada. Vuelva a solicitar una nueva contraseña por favor.'
            })

        # Reset login password error attempts
        user.reset_login_password_error_attempts()

        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    @transaction.non_atomic_requests
    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except Exception as e:
            if e.args is not None and len(e.args) > 1 and e.args[1] == 'no_active_account':
                username = request.data.get("username", None)
                user = User.objects.filter(username=username).first()
                if user is not None:
                    user.register_login_password_error_attempt()
                return Response(
                    {"detail": e.args[0]},
                    status=status.HTTP_400_BAD_REQUEST
                )
            raise e

    # def post(self, request, *args, **kwargs):
    #     serializer = CustomTokenObtainPairSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.validated_data
