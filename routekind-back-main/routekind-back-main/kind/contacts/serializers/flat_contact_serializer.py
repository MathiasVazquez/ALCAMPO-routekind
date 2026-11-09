
from rest_framework import serializers

from kind.contacts.models import Contact
from kind.generics.serializers.base_seriaizer import BaseSerializer


class FlatContactSerializer(BaseSerializer):
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Contact
        fields = '__all__'
