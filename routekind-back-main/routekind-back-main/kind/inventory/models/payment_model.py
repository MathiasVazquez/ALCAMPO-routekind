

from django.db import models

from kind.generics.models.base_model import CustomModelAbstract
from kind.transactions.models.transation_payment_model import TransactionPaymentAbstract


class SaleCondition(CustomModelAbstract):
    name = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Sale condition'
        verbose_name_plural = 'Sale conditions'

    def __str__(self):
        return f'{self.name}'


class SalePayment(TransactionPaymentAbstract):
    # TODO: Add foreign key with Sale
    pass
