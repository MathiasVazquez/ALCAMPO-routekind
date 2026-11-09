from django.db import models

from kind.custom_fields.crypted_json_field import CryptedJSONField
from kind.generics.models.base_model import CustomModelAbstract
from kind.inventory.mixins.price_list_mixin import PriceListMixin
from encrypted_model_fields.fields import EncryptedCharField


class Contact(CustomModelAbstract, PriceListMixin):
    auto_id = models.BigIntegerField(default=0)
    first_name = EncryptedCharField(max_length=510)
    last_name = EncryptedCharField(max_length=510, blank=True, null=True)
    document = EncryptedCharField(max_length=60, blank=True, null=True)
    additional_values = CryptedJSONField(default=dict, blank=True)
    addresses: models.Manager

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def on_create(self):
        self.auto_id = self.company.contacts_auto_enumeration + 1
        self.company.contacts_auto_enumeration = self.auto_id
        self.company.save()

    def __str__(self) -> str:
        return self.full_name

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.on_create()
        return super().save(*args, **kwargs)


# @receiver(m2m_changed, sender=Contact.addresses.through)
# def addresses_changed(sender, instance: Contact, action, pk_set, **kwargs):
#     if action == "post_add":
#         instance.on_address_added(added_addresses_ids=pk_set)
