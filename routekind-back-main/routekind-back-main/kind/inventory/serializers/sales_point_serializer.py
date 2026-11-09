
from kind.inventory.models import SalesPoint
from kind.generics.serializers import BaseSerializer
from kind.inventory.serializers.warehouse_serializer import WarehouseSerializer
from kind.sales.serializers import InvoiceSettingSerializer


class SalesPointSerializer(BaseSerializer):
    # invoice_settings = InvoiceSettingSerializer(many=True, required=False)
    active_invoice_setting = InvoiceSettingSerializer(many=False, required=False)
    warehouse = WarehouseSerializer(many=False, required=False)

    class Meta:
        fields = '__all__'
        model = SalesPoint
