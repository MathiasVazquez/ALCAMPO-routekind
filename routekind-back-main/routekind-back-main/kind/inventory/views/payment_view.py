
from kind.inventory.serializers import PaymentMethodSerializer, SaleConditionSerializer, SalePaymentSerializer
from kind.generics.views.base_view import BaseModelViewSet


class PaymentMethodView(BaseModelViewSet):
    serializer_class = PaymentMethodSerializer


class SaleConditionView(BaseModelViewSet):
    serializer_class = SaleConditionSerializer


class SalePaymentView(BaseModelViewSet):
    serializer_class = SalePaymentSerializer
