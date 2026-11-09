from typing import TYPE_CHECKING

from django.db import models

from kind.generics.models.base_model import CustomModelAbstract

if TYPE_CHECKING:
    from kind.inventory.models import SalesPoint


class InvoiceSetting(CustomModelAbstract):
    # TODO: Unique: company, number, enumeration
    number = models.CharField(max_length=250)  # Timbrado
    # enumeration = models.CharField(max_length=250)
    enumeration_prefix = models.CharField(max_length=250, default='', blank=True)
    enumeration_postfix = models.CharField(max_length=250, default='', blank=True)
    start_date = models.DateField(null=True, blank=True, default=None)
    due_date = models.DateField(null=True, blank=True, default=None)
    sales_point: 'SalesPoint' = models.ForeignKey(
        'inventory.SalesPoint',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='invoice_settings'
    )

    # Auto enumeration fields
    manage_auto_enumeration = models.BooleanField(default=True)
    next_auto_enumeration = models.IntegerField(default=1)
    max_auto_enumeration = models.IntegerField(default=10000)
    enumeration_pad_length = models.IntegerField(default=0)

    invoices: models.Manager

    @property
    def formated_next_auto_enumeration(self):
        padded = f'{self.next_auto_enumeration}'.rjust(self.enumeration_pad_length or 0, "0")
        return f'{self.enumeration_prefix or ""}{padded}{self.enumeration_postfix}'

    class Meta:
        verbose_name = 'Invoice setting'
        verbose_name_plural = 'Invoices settings'

    def autoenumerate(self):
        if not self.manage_auto_enumeration:
            raise ValueError({
                "error": "This invoice setting is not autoenumerable."
            })
        if self.next_auto_enumeration == self.max_auto_enumeration:
            raise ValueError({
                "enumeration": "The enumeration already reach the max value."
            })
        self.next_auto_enumeration += 1
        self.save()

    def __str__(self):
        return f'{self.number} ({self.company.name})'
