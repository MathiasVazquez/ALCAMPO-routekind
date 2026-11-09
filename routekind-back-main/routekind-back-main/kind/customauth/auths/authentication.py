from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import ValidationError

from kind.customauth.models import AuthToken, User


class CustomJWTAuthentication(JWTAuthentication):

    def authenticate(self, request):
        result = super().authenticate(request)
        if not result:
            return None

        [user, token] = result
        user: 'User'

        if (
            user.current_temporal_password is not None and 
            user.current_temporal_password.has_expired
        ):
            raise ValidationError({ 'error': 'Contraseña expirada' })

        # Validate the token exists and is active
        auth = AuthToken.get_by_access(str(token))
        if auth is None:
            return None

        return [user, token]
