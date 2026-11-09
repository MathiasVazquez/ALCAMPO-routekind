
from typing import TYPE_CHECKING

from django.db import models

from kind.generics.models.base_model import CustomModelAbstract

if TYPE_CHECKING:
    from kind.inventory.models import Product


class TransactionDetailAbstract(CustomModelAbstract):
    quantity = models.FloatField(default=0)
    unit_price = models.FloatField(default=0)
    product: "Product" = models.ForeignKey(
        'inventory.Product',
        related_name='%(app_label)s_%(class)s_details',
        on_delete=models.PROTECT
    )

    @property
    def total_price(self):
        return self.quantity * self.unit_price

    class Meta:
        abstract = True

    # def __str__(self):
    #     return f'Detail for order with number {self.order.order_number}'
        # return f'({self.id}) For order {self.order.id if self.order else "None"} with Product ({self.product.id if self.product else "None"}) product_name: {self.product.product_name}'
