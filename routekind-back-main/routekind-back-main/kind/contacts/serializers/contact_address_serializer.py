
from rest_framework import serializers

from kind.addresses.serializers import AddressSerializer
from kind.addresses.models import Address
from kind.contacts.serializers import FlatContactSerializer


class ContactAddressSerializer(AddressSerializer):
    contact = FlatContactSerializer(read_only=True)
