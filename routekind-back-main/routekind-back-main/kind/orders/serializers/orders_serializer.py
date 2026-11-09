
from rest_framework import serializers
from kind.contacts.serializers.contact_address_serializer import ContactAddressSerializer
from kind.contacts.serializers.contact_serializer import ContactSerializer
from kind.generics.serializers.base_model_serializer_mixin import CurrentCompanyDefault

from kind.generics.serializers.base_seriaizer import BaseSerializer
from kind.inventory.serializers.payment_serializer import PaymentMethodSerializer, SaleConditionSerializer
from kind.inventory.serializers.price_list_serializer import PriceListSerializer

from kind.orders.models import Order, OrderDetail, OrderPayment
from kind.sales.serializers import InvoiceSerializer
from kind.inventory.serializers import ProductSerializer


class OrderDetailSerializer(BaseSerializer):
    company = serializers.HiddenField(default=CurrentCompanyDefault())
    product = ProductSerializer(many=False, required=False)
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = OrderDetail
        fields = '__all__'


class OrderPaymentSerializer(BaseSerializer):
    company = serializers.HiddenField(default=CurrentCompanyDefault())
    method = PaymentMethodSerializer(required=False, many=False)
    method_name = serializers.ReadOnlyField()

    class Meta:
        model = OrderPayment
        fields = '__all__'


class OrderSerializer(BaseSerializer):
    company = serializers.HiddenField(default=CurrentCompanyDefault())
    details = OrderDetailSerializer(many=True, required=False)
    payments = OrderPaymentSerializer(many=True, required=False)
    canceled_invoices = InvoiceSerializer(many=True, required=False)
    invoice = InvoiceSerializer(many=False, required=False)
    total_price = serializers.ReadOnlyField()
    is_invoiced = serializers.ReadOnlyField()
    is_partial = serializers.ReadOnlyField()
    total_balance = serializers.ReadOnlyField()
    contact_address = ContactAddressSerializer(many=False, required=False)
    sale_condition = SaleConditionSerializer(many=False, required=False)
    price_list = PriceListSerializer(many=False, required=False)
    contact = serializers.SerializerMethodField()

    def get_contact(self, instance: 'Order'):
        return ContactSerializer(instance.contact).data

    class Meta:
        model = Order
        fields = '__all__'
