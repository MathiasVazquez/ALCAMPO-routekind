
from kind.generics.serializers.base_seriaizer import BaseSerializer

from kind.sales.models import InvoiceTemplate


class InvoiceTemplateSerializer(BaseSerializer):

    class Meta:
        model = InvoiceTemplate
        fields = '__all__'
