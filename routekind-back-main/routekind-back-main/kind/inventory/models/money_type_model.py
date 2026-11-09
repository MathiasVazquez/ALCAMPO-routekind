
from django.db import models

from kind.generics.models.base_model import CustomModelAbstract


class MoneyType(CustomModelAbstract):
    name = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=255, null=True, blank=True)
    decimals = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Money type'
        verbose_name_plural = 'Money types'

    def __str__(self):
        return f'{self.name}'
