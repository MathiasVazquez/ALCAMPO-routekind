from typing import TYPE_CHECKING

from django.db import models

from kind.generics.models.base_model import CustomModelAbstract
from kind.custom_fields import CoordsJSONField

if TYPE_CHECKING:
    from kind.inventory.models import Product, Warehouse


class Batch(CustomModelAbstract):
    code = models.CharField(max_length=1024)
    product: 'Product' = models.ForeignKey(
        'inventory.Product',
        on_delete=models.CASCADE,
    )
    warehouse: 'Warehouse' = models.ForeignKey(
        'inventory.Warehouse',
        on_delete=models.CASCADE,
    )
    quantity = models.FloatField(default=0)
    aditional_information = models.JSONField(default=dict, blank=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    manufacture_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Batch'
        verbose_name_plural = 'Batches'

    def __str__(self):
        return f'{self.code} - {self.product}'
