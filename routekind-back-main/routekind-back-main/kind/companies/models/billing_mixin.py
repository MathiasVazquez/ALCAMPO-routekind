from typing import List

from collections.abc import Iterable
from django.db import models
from rest_framework.exceptions import ValidationError


class BillingCompanyMixin(models.Model):
    document = models.CharField(max_length=64, null=True, blank=True)
    country = models.CharField(max_length=64, null=True, blank=True)
    main_address = models.CharField(max_length=256, null=True, blank=True)
    enable_sales_points = models.BooleanField(default=True)
    # TODO: Add more files for billing

    allow_partial_payment = models.BooleanField(default=False)
    invoice_paper_columns = models.IntegerField(default=30)
    invoice_copies: List[str] = models.JSONField(default=["Original"])

    def _validate_invoice_copies(self):
        if (
            type(self.invoice_copies) != list or
            not all([type(name) == str for name in self.invoice_copies])
        ):
            raise ValidationError({"invoice_copies": "This field must be a list of text."})

    def save(self, *args, **kwars):
        self._validate_invoice_copies()
        return super().save(*args, **kwars)

    class Meta:
        abstract = True
