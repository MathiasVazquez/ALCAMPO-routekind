from rest_framework_simplejwt.serializers import TokenVerifySerializer
from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework.exceptions import AuthenticationFailed

from kind.customauth.models import AuthToken


class CustomTokenVerifySerializer(TokenVerifySerializer):

    def is_valid(self, *, raise_exception=False):
        result = super().is_valid(raise_exception=raise_exception)

        token = self.initial_data.get("token")
        auth = AuthToken.get_by_refresh(token)
        if auth is None:
            if raise_exception:
                raise AuthenticationFailed("Refresh token in not valid")
            else:
                return False

        return result


class CustomTokenVerifyView(TokenVerifyView):
    serializer_class = CustomTokenVerifySerializer
