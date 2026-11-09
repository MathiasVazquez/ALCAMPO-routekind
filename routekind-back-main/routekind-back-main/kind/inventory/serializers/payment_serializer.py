
from kind.generics.serializers.base_seriaizer import BaseSerializer

from kind.inventory.models import SalePayment, SaleCondition, PaymentMethod


class SalePaymentSerializer(BaseSerializer):
    class Meta:
        model = SalePayment
        fields = '__all__'


class PaymentMethodSerializer(BaseSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'


class SaleConditionSerializer(BaseSerializer):
    class Meta:
        model = SaleCondition
        fields = '__all__'
