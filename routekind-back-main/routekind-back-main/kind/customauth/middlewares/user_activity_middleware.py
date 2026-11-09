from typing import TYPE_CHECKING

from django.http import HttpRequest
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from kind.customauth.models import AuthToken
from kind.customauth.models.auth_token_model import AUTH_TOKEN_ACCESS

if TYPE_CHECKING:
    from kind.customauth.models import User


class UserLastActivityMiddleware(MiddlewareMixin):
    def _get_user(self, request: HttpRequest):
        authorization: str = request.headers.get('Authorization')
        if not authorization:
            return None

        auth: AuthToken = AuthToken.objects.filter(
            access=authorization.split(' ')[1],
            type=AUTH_TOKEN_ACCESS
        ).first()

        return auth.user if auth else None

    def process_request(self, request: HttpRequest):
        user: User = self._get_user(request)
        if user:
            user.last_activity_date = timezone.now()
            user.save()
