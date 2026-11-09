from typing import TYPE_CHECKING

from django.db import models

from kind.generics.models.generic_base_model import GenericBaseModel

if TYPE_CHECKING:
    from kind.customauth.models import User
    from kind.addresses.models import Address
    from kind.zones.models import Zone
    from kind.tasks.models import Task, TaskStatus


USER_AUDIT_ACTION_TYPE_CHOICES = (
    ('c', 'Create'),
    ('u', 'Update'),
    ('d', 'Delete'),
)


class UserAudit(GenericBaseModel):
    app_name = 'audits'
    created_by: 'User'
    module_name = models.CharField(max_length=35)
    module_instance_id = models.CharField(max_length=510, blank=True, null=True)
    module_instance_code = models.BigIntegerField(default=0)
    entry_log = models.CharField(max_length=4000)
    entry_status = models.JSONField(default=dict)
    action_type = models.CharField(max_length=1, choices=USER_AUDIT_ACTION_TYPE_CHOICES, null=True, default=None)
    ip_address = models.CharField(max_length=120)
    device_info = models.CharField(max_length=120, null=True)

    @classmethod
    def add_tasks_log(
        cls,
        instance: 'Task',
        user: 'User',
        ip_address: str,
        device_info: str = None,
        *,
        created: bool = False,
        deleted: bool = False,
        entry_log: str = None,
        entry_status: dict = None
    ):
        action_type = "d" if deleted else "c" if created else "u"
        action_label = "eliminado" if deleted else "creado" if created else "modificado"
        entry_log = entry_log or f'{user.name} (@{user.username}) ha {action_label} la tarea "{instance.subject}"'

        cls.objects.create(
            created_by=user,
            module_name='tasks',
            module_instance_id=instance.id,
            module_instance_code=instance.auto_id,
            entry_log=entry_log,
            company=user.company,
            action_type=action_type,
            ip_address=ip_address,
            device_info=device_info,
            entry_status=entry_status if entry_status is not None else {
                'description': instance.description,
                'users': list(instance.users.values_list('username', flat=True)),
                'start_date': instance.start_date.isoformat() if instance.start_date else None,
                'due_date': instance.due_date.isoformat() if instance.due_date else None,
            },
        )

    @classmethod
    def add_zones_log(
        cls,
        instance: 'Zone',
        user: 'User',
        ip_address: str,
        device_info: str = None,
        *,
        created: bool = False,
        deleted: bool = False,
        entry_log: str = None,
        entry_status: dict = None
    ):
        action_type = "d" if deleted else "c" if created else "u"
        action_label = "eliminado" if deleted else "creado" if created else "modificado"
        entry_log = entry_log or f'{user.name} (@{user.username}) ha {action_label} la zona "{instance.label}"'

        cls.objects.create(
            created_by=user,
            module_name='zones',
            module_instance_id=instance.id,
            module_instance_code=instance.auto_id,
            entry_log=entry_log,
            action_type=action_type,
            company=user.company,
            ip_address=ip_address,
            device_info=device_info,
            entry_status=entry_status if entry_status is not None else {
                'label': instance.label,
                'additional_addresses': list(instance.additional_addresses.values_list('id', flat=True)),
                'excluded_addresses': list(instance.excluded_addresses.values_list('id', flat=True)),
            },
        )

    @classmethod
    def add_users_log(
        cls,
        instance: 'User',
        user: 'User',
        ip_address: str,
        device_info: str = None,
        *,
        created: bool = False,
        deleted: bool = False,
        entry_log: str = None,
        entry_status: dict = None
    ):
        action_type = "d" if deleted else "c" if created else "u"
        action_label = "eliminado" if deleted else "creado" if created else "modificado"
        entry_log = entry_log or f'{user.name} (@{user.username}) ha {action_label} al usuario "{instance.name} (@{instance.username})"'

        cls.objects.create(
            created_by=user,
            module_name='users',
            module_instance_id=instance.id,
            module_instance_code=instance.auto_id,
            entry_log=entry_log,
            action_type=action_type,
            company=user.company,
            ip_address=ip_address,
            device_info=device_info,
            entry_status=entry_status if entry_status is not None else {
                'name': instance.name,
                'isActive': instance.is_active,
            },
        )

    @classmethod
    def add_create_addresses_log(
        cls,
        instance: 'Address',
        user: 'User',
        ip_address: str,
        device_info: str = None,
    ):
        cls.objects.create(
            created_by=user,
            module_name='addresses',
            module_instance_id=instance.id,
            module_instance_code=instance.auto_id,
            entry_log=f'{user.name} (@{user.username}) ha creado el comercio "{instance.description}"',
            company=user.company,
            action_type='c',
            ip_address=ip_address,
            device_info=device_info,
        )

    @classmethod
    def add_task_status_change_log(
        cls,
        instance: 'Task',
        user: 'User',
        status: 'TaskStatus',
        ip_address: str,
        device_info: str = None,
    ):
        cls.add_tasks_log(
            instance,
            user,
            entry_status={},
            entry_log=f'{user.name} (@{user.username}) ha cambiado el estado de la tarea "{instance.subject}" a "{status.label}"',
            ip_address=ip_address,
            device_info=device_info,
        )

    class Meta:
        ordering = ["-created_at"]
