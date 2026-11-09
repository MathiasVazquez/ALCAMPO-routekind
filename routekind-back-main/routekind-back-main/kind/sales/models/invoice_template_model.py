from typing import TYPE_CHECKING

from django.db import models

from kind.generics.models.base_model import CustomModelAbstract
from kind.generics.models.named_model import StrictNamedModelMixin

if TYPE_CHECKING:
    from kind.addresses.models import Address
    from kind.customauth.models import User


class InvoiceTemplate(CustomModelAbstract, StrictNamedModelMixin):
    code = models.CharField(max_length=64000)
    description = models.CharField(max_length=1024, blank=True, default="")

    class Meta:
        verbose_name = 'Invoice template'
        verbose_name_plural = 'Invoices templates'

    def __str__(self):
        return f'{self.name}'
