
from typing import TYPE_CHECKING, List

from django.db import models
from kind.custom_fields.coords_field import CoordsJSONField

from kind.generics.models.base_model import CustomModelAbstract
from kind.inventory.mixins import PriceListMixin, WarehouseMixin

if TYPE_CHECKING:
    from kind.sales.models import InvoiceSetting


class SalesPoint(
    CustomModelAbstract,
    PriceListMixin,
    WarehouseMixin,
):
    app_name = 'salespoint'
    name = models.CharField(max_length=120)
    active_invoice_setting: 'InvoiceSetting' = models.ForeignKey(
        'sales.InvoiceSetting',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='sales_point_actives_at'
    )
    users: models.Manager

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Sales point"
        verbose_name_plural = "Sales points"
