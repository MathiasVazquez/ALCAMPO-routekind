
from rest_framework import serializers

from kind.generics.serializers.base_seriaizer import BaseSerializer

from kind.sales.models import InvoiceSetting


class InvoiceSettingSerializer(BaseSerializer):

    formated_next_auto_enumeration = serializers.ReadOnlyField()

    class Meta:
        model = InvoiceSetting
        fields = '__all__'
