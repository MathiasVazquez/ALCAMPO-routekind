
from kind.generics.serializers.base_seriaizer import BaseSerializer

from kind.inventory.models import MoneyType


class MoneyTypeSerializer(BaseSerializer):
    class Meta:
        model = MoneyType
        fields = '__all__'
