
from kind.addresses.serializers.address_serializer import AddressSerializer
from kind.contacts.serializers.flat_contact_serializer import FlatContactSerializer


class ContactSerializer(FlatContactSerializer):
    addresses = AddressSerializer(many=True, required=False)
