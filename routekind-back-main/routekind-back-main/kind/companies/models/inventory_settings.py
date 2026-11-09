
from typing import TYPE_CHECKING

from django.db import models

if TYPE_CHECKING:
    from kind.inventory.models import MoneyType

ALL_PRICE_LIST_SOURCE = 'all'
CONTACT_PRICE_LIST_SOURCE = 'contact'
USER_PRICE_LIST_SOURCE = 'user'
PRICE_LIST_SOURCE_CHOICES = (
    (ALL_PRICE_LIST_SOURCE, ALL_PRICE_LIST_SOURCE),
    (CONTACT_PRICE_LIST_SOURCE, CONTACT_PRICE_LIST_SOURCE),
    (USER_PRICE_LIST_SOURCE, USER_PRICE_LIST_SOURCE),
)

# MONEY_TYPE_PRIORITY_PRICE_LIST = "price_list"
# MONEY_TYPE_PRIORITY_PRODUCT = "product"
# MONEY_TYPE_PRIORITY_COMPANY = "company"
# MONEY_TYPE_PRIORITY_CHOICES = (
#     (MONEY_TYPE_PRIORITY_PRICE_LIST, MONEY_TYPE_PRIORITY_PRICE_LIST),
#     (MONEY_TYPE_PRIORITY_PRODUCT, MONEY_TYPE_PRIORITY_PRODUCT),
#     (MONEY_TYPE_PRIORITY_COMPANY, MONEY_TYPE_PRIORITY_COMPANY),
# )

EDIT_PAYMENT_CHOICES = (
    ('all', 'all'),
    ('add', 'add'),
    ('remove', 'remove'),
    ('confirm', 'confirm'),
    ('none', 'none'),
)


class CompanyInventorySettingsMixin(models.Model):
    price_list_source = models.CharField(
        choices=PRICE_LIST_SOURCE_CHOICES,
        default=ALL_PRICE_LIST_SOURCE,
        max_length=12,
    )
    default_money_type: "MoneyType" = models.ForeignKey(
        'inventory.MoneyType',
        default=None,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='default_in_companies'
    )
    decimal_separator = models.CharField(max_length=1, default=',')
    number_separator = models.CharField(max_length=1, default='.')
    allow_edit_payments_on_sale = models.CharField(max_length=8, default='none', choices=EDIT_PAYMENT_CHOICES)
    # money_type_priority = models.CharField(
    #     max_length=12,
    #     choices=MONEY_TYPE_PRIORITY_CHOICES,
    #     default=MONEY_TYPE_PRIORITY_PRICE_LIST,
    # )

    class Meta:
        abstract = True
