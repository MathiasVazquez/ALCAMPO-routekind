from typing import TYPE_CHECKING

from django.db import models
from rest_framework.exceptions import ValidationError

from kind.generics.models.base_model import CustomModelAbstract
from kind.custom_fields import CoordsJSONField

if TYPE_CHECKING:
    from kind.inventory.models import Product


class Warehouse(CustomModelAbstract):
    name = models.CharField(max_length=1024)
    coords: dict = CoordsJSONField(default=None, null=True, blank=True)
    details: models.Manager
    # track_batches = models.BooleanField(default=False)
    # track_inventory = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Warehouse'
        verbose_name_plural = 'Warehouses'

    def __str__(self):
        return f'{self.name}'


class WarehouseProductDetail(CustomModelAbstract):
    warehouse = models.ForeignKey(
        Warehouse,
        related_name='details',
        on_delete=models.CASCADE,
    )
    product: 'Product' = models.ForeignKey(
        'inventory.Product',
        related_name='warehouse_details',
        on_delete=models.CASCADE,
    )
    available_quantity = models.FloatField(default=0)

    class Meta:
        verbose_name = 'Warehouse detail'
        verbose_name_plural = 'Warehouses details'
        unique_together = ('warehouse', 'product')

    def save(self, *args, **kwargs):
        if not self.product.track_inventory:
            raise ValidationError(f"Product '{self.product}' do not track inventory.")
        if self.product.track_batches:
            raise ValidationError(f"Product '{self.product}' do track batches. Use batches instead details.")
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.warehouse} - {self.product} : {self.available_quantity}'
