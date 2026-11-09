from typing import List, TYPE_CHECKING

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType

from kind.companies.models.api_settings_mixin import ApiSettingsCompanyMixin
from kind.companies.models.billing_mixin import BillingCompanyMixin
from kind.companies.models.inventory_settings import CompanyInventorySettingsMixin
from kind.companies.models.task_settings import CompanyTaskSettingsMixin

# Base model
from kind.generics.models import GenericBaseModel
from kind.connections.models import ApiConnectionModule, ApiConnectionModuleWebhook

if TYPE_CHECKING:
    from kind.connections.models import ApiConnection


class Company(
    GenericBaseModel,
    BillingCompanyMixin,
    ApiSettingsCompanyMixin,
    CompanyInventorySettingsMixin,
    CompanyTaskSettingsMixin,
):
    name = models.CharField(max_length=128, null=True, blank=True)
    email = models.EmailField(max_length=64, null=True, blank=True)
    max_users = models.PositiveIntegerField(default=1)

    customauth_user_instances: models.Manager

    coords_raw_formatter = models.JSONField(default=None, blank=True, null=True)
    prefabricated_map_zones = models.JSONField(default=None, blank=True, null=True)

    contact_custom_fields_meta = models.JSONField(default=None, blank=True, null=True)
    address_custom_fields_meta = models.JSONField(default=None, blank=True, null=True)

    label_replacements = models.JSONField(default=None, blank=True, null=True)
    require_change_password_at_first_login = models.BooleanField(default=False)

    # TODO: implement (currently is taken like always true)
    use_temporal_new_passwords = models.BooleanField(default=False)
    default_temporal_new_passwords_lifetime_hours = models.IntegerField(default=24)

    allow_registers_without_coords = models.BooleanField(default=False)

    users_auto_enumeration = models.BigIntegerField(default=0)
    addresses_auto_enumeration = models.BigIntegerField(default=0)
    contacts_auto_enumeration = models.BigIntegerField(default=0)
    tasks_auto_enumeration = models.BigIntegerField(default=0)
    zones_auto_enumeration = models.BigIntegerField(default=0)
    polygons_auto_enumeration = models.BigIntegerField(default=0)
    audits_auto_enumeration = models.BigIntegerField(default=0)

    max_get_audit_registers = models.IntegerField(default=1000)

    api_connections: models.Manager

    def get_api_connection_webhooks_by_model(self, model_class, *, on_action=None):
        modules = self.get_api_connection_modules_by_model(model_class)
        webhooks_qs = ApiConnectionModuleWebhook.objects.filter(
            connection_module__in=modules.all()
        )
        if on_action is not None:
            webhooks_qs = webhooks_qs.filter(on_action=on_action)

        return webhooks_qs

    def get_api_connection_modules_by_model(self, model_class):
        content_type = ContentType.objects.get_for_model(model_class)
        return ApiConnectionModule.objects.filter(
            content_type=content_type,
            connection__in=self.api_connections.all()
            # connection__id__in=self.api_connections.values_list('id', flat=True)
        )
        # for connection in self.api_connections.all():
        #     connection: 'ApiConnection'
        #     module = connection.get_module(model_class)
        #     if module is None:
        #         continue

    @property
    def active_users_count(self):
        users = self.customauth_user_instances
        return users.filter(is_active=True).count()

    @property
    def allow_more_users(self):
        return self.active_users_count < self.max_users

    # DEFAULS
    default_date_format = models.CharField(max_length=64, default='YYYY-MM-DD')
    default_orders_task_template = models.ForeignKey(
        'tasks.StatusFlowTemplate',
        null=True,
        blank=True,
        # related_name='%(app_label)s_%(class)s_orders_tasks_companies_default',
        related_name='orders_tasks_flow_companies_default',
        on_delete=models.SET_NULL,
    )
    default_invoices_task_template = models.ForeignKey(
        'tasks.StatusFlowTemplate',
        null=True,
        blank=True,
        related_name='invoices_tasks_flow_companies_default',
        on_delete=models.SET_NULL,
    )
    default_tasks_template = models.ForeignKey(
        'tasks.StatusFlowTemplate',
        null=True,
        blank=True,
        related_name='tasks_flow_companies_default',
        on_delete=models.SET_NULL,
    )

    @property
    def users(self):
        from kind.customauth.models import User
        return User.objects.filter(company=self)

    def __str__(self) -> str:
        return f'({self.id}) {self.name}'

    def save(self, *args, **kwargs):
        if not self.coords_raw_formatter:
            self.coords_raw_formatter = [
                {
                    "name": "region",
                    "label": "Región"
                },
                {
                    "name": "state",
                    "label": "Departamento"
                },
                {
                    "name": "city",
                    "label": "Ciudad"
                },
                {
                    "name": "neighbourhood",
                    "label": "Barrio"
                }
            ]

        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")
