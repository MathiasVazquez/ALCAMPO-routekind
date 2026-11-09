from typing import TYPE_CHECKING

from django.db import models

from kind.generics.models.base_model import CustomModelAbstract
from kind.custom_fields import CoordsJSONField

if TYPE_CHECKING:
    from kind.inventory.models import Product, MoneyType


class PriceList(CustomModelAbstract):
    name = models.CharField(max_length=255, null=True, blank=True)
    money_type: "MoneyType" = models.ForeignKey(
        'inventory.MoneyType',
        default=None,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='default_in_pricelists'
    )
    details: models.Manager

    class Meta:
        verbose_name = 'Price list'
        verbose_name_plural = 'Price lists'

    def __str__(self):
        return f'{self.name}'


class PriceListDetail(CustomModelAbstract):
    product = models.ForeignKey(
        'inventory.Product',
        on_delete=models.CASCADE
    )
    price_list: 'Product' = models.ForeignKey(
        PriceList, on_delete=models.CASCADE,
        related_name="details"
    )
    unit_price = models.FloatField(default=0)

    def __str__(self):
        return f'({self.id}) {self.product} -> {self.unit_price}'
