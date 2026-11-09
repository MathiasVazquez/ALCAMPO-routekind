
from kind.generics.serializers.base_seriaizer import BaseSerializer

from kind.inventory.models import PriceList, PriceListDetail
from kind.inventory.serializers.money_type_serializer import MoneyTypeSerializer


class PriceListDetailSerializer(BaseSerializer):
    class Meta:
        model = PriceListDetail
        fields = '__all__'


class PriceListSerializer(BaseSerializer):
    details = PriceListDetailSerializer(many=True, required=False)
    money_type = MoneyTypeSerializer(many=False, required=False)

    class Meta:
        model = PriceList
        fields = '__all__'
