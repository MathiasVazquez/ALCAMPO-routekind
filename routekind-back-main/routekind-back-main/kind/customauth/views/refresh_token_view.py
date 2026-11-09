# Rest Framework
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.exceptions import AuthenticationFailed

# Models
from kind.customauth.models import AuthToken


class CustomTokenRefreshSerializer(TokenRefreshSerializer):

    def get_auth(self, refresh):

        # Validate the token exists and is active
        auth = AuthToken.objects.filter(refresh=refresh).first()
        if auth is None or not auth.is_active:
            return None

        return auth

    def is_valid(self, *, raise_exception=False):
        result = super().is_valid(raise_exception=raise_exception)

        # Validate refresh token
        auth = AuthToken.get_by_refresh(self.initial_data.get("refresh"))
        if auth is None:
            if raise_exception:
                raise AuthenticationFailed(f"Refresh token in not valid")
            else:
                return False

        return result

    def validate(self, attrs):
        result = super().validate(attrs)

        # Update database access token on refresh
        auth = AuthToken.get_by_refresh(attrs.get("refresh"))
        if auth is not None:
            auth.access = result.get("access")
            auth.save()

        return result


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer
