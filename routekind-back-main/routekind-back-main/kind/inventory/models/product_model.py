
from django.db import models

from kind.generics.models.base_model import CustomModelAbstract


class Measurement(CustomModelAbstract):
    name = models.CharField(max_length=1024)

    class Meta:
        verbose_name = 'Measurement'
        verbose_name_plural = 'Measurements'

    def __str__(self):
        return f'{self.name}'


class Tax(CustomModelAbstract):
    name = models.CharField(max_length=1024)
    percentage = models.FloatField(default=0)

    class Meta:
        verbose_name = 'Tax'
        verbose_name_plural = 'Taxs'

    def __str__(self):
        return f'{self.name}'


PRODUCT_TYPE_CHOICES = (
    ('g', 'Good'),
    ('s', 'Service')
)


class Product(CustomModelAbstract):

    name = models.CharField(max_length=1024)
    description = models.CharField(max_length=2040, blank=True, default='')
    code = models.CharField(max_length=250, blank=True, default=None, null=True)
    sku = models.CharField(max_length=250, blank=True, default=None, null=True)
    type = models.CharField(choices=PRODUCT_TYPE_CHOICES, max_length=1, blank=True, default=None, null=True)

    # Mover a Measurement, o a price list?
    unit_variation = models.FloatField(default=1)
    unit_decimals = models.IntegerField(default=0)
    ######

    track_batches = models.BooleanField(default=False)
    track_inventory = models.BooleanField(default=False)
    aditional_information = models.JSONField(default=dict, blank=True)
    unit_measurement = models.ForeignKey(
        Measurement,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    taxes = models.ManyToManyField(
        Tax,
        blank=True,
    )
    warehouse_details: models.Manager

    @property
    def total_availability(self):
        return self.warehouse_details.aggregate(
            _total=models.Sum(models.F("available_quantity"))
        )['_total']

    def save(self, *args, **kwargs):

        # Remove warehouse details on remove track inventory (?)
        if not self.track_inventory and hasattr(self, "warehouse_details"):
            _warehouse_details: models.Manager = getattr(self, "warehouse_details")
            if issubclass(_warehouse_details.__class__, models.Manager):
                _warehouse_details.all().delete()

        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return f'{self.name}'
