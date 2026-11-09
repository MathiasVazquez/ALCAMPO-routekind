
from typing import TYPE_CHECKING

from django.db import models

if TYPE_CHECKING:
    from kind.inventory.models import Warehouse


class WarehouseMixin(models.Model):
    warehouse: "Warehouse" = models.ForeignKey(
        'inventory.Warehouse',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='warehouses',
    )

    class Meta:
        abstract = True
