from django.db import models
from django.utils.translation import gettext_lazy as _
from django.apps import apps
from rest_framework.exceptions import ValidationError

from kind.generics.models.base_model import GenericBaseModel
from kind.generics.models.named_model import StrictNamedModelMixin


PERMISSIONS_DATA = {
    'users': ['status', 'reset-password'],
    'roles': ['assign'],
    'addresses': [],
    'contacts': [],
    'tasks': ['list-own', 'update-own', 'interact'],
    'flows': [],
    'activities': ['list-own'],
    'zones': ['list-own'],
    'orders': [],
    'salespoint': [],
    'invoices': ['cancel', 'print', 'reprint'],
    'companies': ['profile'],
    'audits': [''],
}

DEFAULT_PERMISSIONS_ACTIONS = [
    'all',
    'create',
    'update',
    'delete',
    'list',
]


class RoleManager(models.Manager):
    @classmethod
    def get_valid_permissions(self):
        result = []
        for key, values in PERMISSIONS_DATA.items():
            for value in [*DEFAULT_PERMISSIONS_ACTIONS, *values]:
                result.append(f"{key}.{value}")
        return result


class RoleAbstract(GenericBaseModel, StrictNamedModelMixin):
    app_name = 'roles'
    description = models.CharField(max_length=1020, blank=True, default='')
    permissions: list = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_("permissions")
    )
    users = models.ManyToManyField(
        'customauth.User',
        related_name='roles',
        blank=True
    )

    objects = RoleManager()

    def clean_permissions(self):
        # Check data type
        if type(self.permissions) != list:
            raise ValidationError({'permissions': 'This field must be a list'})

        # Check valid permissions
        valid_permissions = RoleManager.get_valid_permissions()
        for permission in self.permissions:
            if permission not in valid_permissions:
                raise ValidationError({'permission': f'{permission} is not a valid permission.'})

    def has_permission(self, permission: str):
        return permission in self.permissions

    def save(self, *args, **kwargs):
        # Check that permissions are valid
        self.clean_permissions()
        # Save
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True
        verbose_name = _("role")
        verbose_name_plural = _("roles")

    def __str__(self):
        return self.name
