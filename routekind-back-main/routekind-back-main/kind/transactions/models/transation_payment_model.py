from typing import TYPE_CHECKING
from datetime import datetime

from django.db import models

from kind.generics.models.base_model import CustomModelAbstract

if TYPE_CHECKING:
    from kind.inventory.models import PaymentMethod


class TransactionPaymentAbstract(CustomModelAbstract):
    # TODO: Other info...
    amount = models.FloatField(default=0)
    confirmed = models.BooleanField(default=True)
    method: "PaymentMethod" = models.ForeignKey(
        "inventory.PaymentMethod",
        related_name='%(app_label)s_%(class)s_payments',
        on_delete=models.PROTECT
    )
    datetime = models.DateTimeField(default=datetime.now)

    @property
    def method_name(self):
        return self.method.name

    class Meta:
        abstract = True
