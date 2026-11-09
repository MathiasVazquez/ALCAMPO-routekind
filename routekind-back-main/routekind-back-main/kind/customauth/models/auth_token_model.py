from typing import Union, TYPE_CHECKING
from django.db import models
from django.conf import settings

from kind.generics.models.base_model import CustomModelAbstract

if TYPE_CHECKING:
    from kind.connections.models.api_connection_model import ApiConnection
    from kind.customauth.models import User

AUTH_TOKEN_ACCESS = "acc"
AUTH_TOKEN_API = "api"

AUTH_TOKEN_CHOICES = (
    (AUTH_TOKEN_ACCESS, 'Access'),
    (AUTH_TOKEN_API, 'API')
)


class AuthToken(CustomModelAbstract):
    created_by = None
    updated_by = None
    access = models.CharField("Access", max_length=2048, unique=True)
    refresh = models.CharField("Refresh", max_length=2048, unique=True)
    user: 'User' = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='jwt_auth_tokens',
        on_delete=models.CASCADE,
        verbose_name="User"
    )
    type = models.CharField(
        max_length=3,
        choices=AUTH_TOKEN_CHOICES,
        default=AUTH_TOKEN_ACCESS
    )
    connection: 'ApiConnection'

    @classmethod
    def get_by_refresh(cls, refresh: str) -> Union['AuthToken', None]:
        return AuthToken.objects.filter(
            refresh=refresh,
            is_active=True
        ).first()

    @classmethod
    def get_by_access(cls, access: str) -> Union['AuthToken', None]:
        return AuthToken.objects.filter(
            access=access,
            is_active=True
        ).first()

    def __str__(self) -> str:
        return f'({self.id}) {self.user.username} ({self.type})'

    class Meta:
        # constraints = [
        #   models.UniqueConstraint(fields=['refresh', 'user'], name='Unique user-refreshtoken')
        # ]
        verbose_name = "JwToken"
        verbose_name_plural = "JwTokens"
        unique_together = ('user', 'type')
