
from django.db import models
from rest_framework.exceptions import ValidationError

from kind.generics.models.base_model import CustomModelAbstract


class CustomTransactionAbstract(CustomModelAbstract):
    details: models.Manager
    payments: models.Manager

    @property
    def is_partial(self):
        return self.total_balance > 0

    @property
    def total_balance(self):
        return self.total_price - self.total_payed

    @property
    def total_price(self):
        return self.details.aggregate(
            total=models.Sum(models.F('quantity') * models.F('unit_price'))
        )['total'] or 0

    @property
    def total_payed(self):
        return self.payments.aggregate(
            total=models.Sum(models.F('amount'))
        )['total'] or 0

    def _validate_balance_gte_zero(self):
        if self.total_balance < 0:
            raise ValidationError({
                "error": f"Total Payed ({self.total_payed}) cannot be greater than Total Price ({self.total_price})"
            })

    def save(self, *args, **kwargs):
        # self._validate_balance_gte_zero()
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True
