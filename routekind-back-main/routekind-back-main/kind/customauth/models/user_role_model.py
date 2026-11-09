from django.utils.translation import gettext_lazy as _
from django.db import models

from .role_abstract import RoleAbstract


class UserRole(RoleAbstract):
    restricted_to_user_roles = models.ManyToManyField(
        'self',
        blank=True,
        null=True,
        default=None,
        symmetrical=False,
    )

    class Meta:
        verbose_name = _("User role")
        verbose_name_plural = _("User roles")
