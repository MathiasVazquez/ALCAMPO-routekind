
from django.db import models


class PriceListMixin(models.Model):
    price_lists = models.ManyToManyField(
        'inventory.PriceList',
        blank=True
    )

    class Meta:
        abstract = True
