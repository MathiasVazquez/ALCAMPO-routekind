from typing import TYPE_CHECKING, List

from django.db import models
from django.db.models import Count
from django.db.models.expressions import Func

if TYPE_CHECKING:
    from kind.customauth.models import UserRole, User
    from kind.companies.models import Company


class UserRoleMixin:
    roles: models.Manager
    is_superuser: bool
    company: 'Company'

    def has_permission(self, permission: str, *, exact=False):
        if self.is_superuser:
            return True

        module_all_permission = f"{permission.split('.')[0]}.all"

        if exact:
            qs = self.roles.filter(permissions__contains=permission)
        else:
            qs = self.roles.filter(
                models.Q(permissions__contains=permission) |
                models.Q(permissions__contains=f"{permission}-own") |
                models.Q(permissions__contains=module_all_permission)
            )

        return qs.count() > 0

    def has_permissions(self, permissions: List[str]):
        # Para cada permiso en 'permissions', creamos un Q object y sumamos un '1' por cada coincidencia.
        aggregated_query = sum([
            Count(
                'pk',
                filter=models.Q(permissions__contains=[perm]),
                distinct=True
            ) for perm in permissions
        ])

        # Calcula el total de coincidencias
        matching_perms_count = (
            self.roles.aggregate(
                total=aggregated_query
            )['total']
        )

        # Retorna True si el número de permisos coincidentes es igual al número de permisos requeridos
        return matching_perms_count == len(permissions)

    def has_role(self, role: 'UserRole'):
        return self.roles.filter(id=role.id).exists()

    def add_role(self, role: 'UserRole'):
        role.users.add(self)

    def get_restricted_to_roles(self):
        qs_is_restricted_to = None
        for role in self.roles.all():
            role: 'UserRole'
            restricted_roles = role.restricted_to_user_roles.all()
            if restricted_roles is None or restricted_roles.count() == 0:
                qs_is_restricted_to = None
                break

            if qs_is_restricted_to is None:
                qs_is_restricted_to = restricted_roles
            else:
                qs_is_restricted_to = qs_is_restricted_to | restricted_roles

        return qs_is_restricted_to

    def filter_users_by_restricted_roles(self, users_qs: 'models.QuerySet'):
        qs_is_restricted_to = self.get_restricted_to_roles()
        if qs_is_restricted_to is not None:
            restricted_to_roles_ids = qs_is_restricted_to.values_list('id', flat=True)
            users_qs = users_qs.filter(roles__id__in=restricted_to_roles_ids)
        return users_qs


class AssignableMixin(models.Model):
    users = models.ManyToManyField(
        'customauth.User',
        blank=True,
        related_name='%(app_label)s_%(class)s_assigned_users',
    )
    sales_points = models.ManyToManyField(
        'inventory.SalesPoint',
        blank=True,
        related_name='%(app_label)s_%(class)s_assigned_salespoints',
    )
    # TODO: ADD USER GROUP

    def is_user_assigned(self, user: 'User'):
        directed_assigned = self.users.filter(id=user.id).exists()
        if directed_assigned:
            return True

        user_sales_point = user.assigned_sales_point
        if user_sales_point:
            is_in_sales_point = self.sales_points.filter(id=user_sales_point.id).exists()
            if is_in_sales_point:
                return True

        # TODO: VALIDATE USER GROUP

        return False

    class Meta:
        abstract = True
