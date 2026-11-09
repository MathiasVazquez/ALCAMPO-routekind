
from django.db import models

from kind.generics.models.base_model import CustomModelAbstract


class PaymentMethod(CustomModelAbstract):
    name = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Payment method'
        verbose_name_plural = 'Payment methods'

    def __str__(self):
        return f'{self.name}'
