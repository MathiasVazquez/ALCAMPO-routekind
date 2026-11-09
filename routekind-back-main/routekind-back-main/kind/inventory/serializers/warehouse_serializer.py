
from kind.generics.serializers.base_seriaizer import BaseSerializer

from kind.inventory.models import Warehouse, WarehouseProductDetail


class WarehouseProductDetailSerializer(BaseSerializer):

    class Meta:
        model = WarehouseProductDetail
        fields = '__all__'


class WarehouseSerializer(BaseSerializer):
    details = WarehouseProductDetailSerializer(required=False, many=True)

    class Meta:
        model = Warehouse
        fields = '__all__'
