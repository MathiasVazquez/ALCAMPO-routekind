
from rest_framework import serializers

from kind.addresses.serializers.address_serializer import AddressSerializer
from kind.contacts.serializers.contact_serializer import ContactSerializer
from kind.generics.serializers.base_seriaizer import BaseSerializer
from kind.inventory.serializers.payment_serializer import PaymentMethodSerializer, SaleConditionSerializer
from kind.inventory.serializers.product_serializer import ProductSerializer

from kind.sales.models import InvoiceDetail, InvoicePayment, Invoice
from kind.sales.serializers.invoice_setting_serializer import InvoiceSettingSerializer
from kind.utils import create_dynamic_fields_serializer


class InvoiceDetailSerializer(BaseSerializer):

    def set_originals(self):
        instance: InvoiceDetail = self.instance
        product_seiralizer = create_dynamic_fields_serializer(
            ProductSerializer, (
                "id",
                "taxes",
                "unit_measurement",
                "name",
                "description",
                "unit_variation",
                "unit_decimals",
                "track_batches",
                "track_inventory",
            )
        )
        instance.original_product = product_seiralizer(instance.product).data
        instance.save()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["product"] = data.pop("original_product")
        return data

    class Meta:
        model = InvoiceDetail
        fields = '__all__'


class InvoicePaymentSerializer(BaseSerializer):

    method_name = serializers.ReadOnlyField()

    def set_originals(self):
        instance: "InvoicePayment" = self.instance
        method_seiralizer = create_dynamic_fields_serializer(
            PaymentMethodSerializer, ("id", "name")
        )
        instance.original_method = method_seiralizer(instance.method).data
        instance.save()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["method"] = data.pop("original_method")
        return data

    class Meta:
        model = InvoicePayment
        fields = '__all__'


class InvoiceSerializer(BaseSerializer):

    details = InvoiceDetailSerializer(many=True, required=False)
    payments = InvoicePaymentSerializer(many=True, required=False)
    # tasks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    tasks = serializers.SerializerMethodField()

    def get_tasks(self, instance: 'Invoice'):
        return [str(id) for id in instance.tasks.values_list('id', flat=True)]

    def set_originals(self, instance: "Invoice"):
        # Save original address
        address_seiralizer = create_dynamic_fields_serializer(
            AddressSerializer, ("id", "description", "coords")
        )
        instance.original_address = address_seiralizer(instance.contact_address).data

        # Save original sales point
        from kind.inventory.serializers import SalesPointSerializer
        sales_point_serializer = create_dynamic_fields_serializer(
            SalesPointSerializer, (
                "id",
                "name",
            )
        )
        instance.original_sales_point = sales_point_serializer(instance.sales_point).data

        # Save original user
        from kind.customauth.serializers.user_serializer import UserSerializer
        user_serializer = create_dynamic_fields_serializer(
            UserSerializer, (
                "id",
                "username",
            )
        )
        instance.original_user = user_serializer(instance.user).data

        # Save original contact
        contact_seiralizer = create_dynamic_fields_serializer(
            ContactSerializer, (
                "id",
                "first_name",
                "last_name",
                "document",
                "full_name",
            )
        )
        instance.original_contact = contact_seiralizer(instance.contact).data

        # Save original sale condition
        condition_seiralizer = create_dynamic_fields_serializer(
            SaleConditionSerializer, (
                "id",
                "name",
                "code",
            )
        )
        instance.original_sale_condition = condition_seiralizer(instance.sale_condition).data

        # Save original settings
        settings_serializer = create_dynamic_fields_serializer(
            InvoiceSettingSerializer, (
                "id",
                "number",
                "start_date",
                "due_date",
            )
        )
        instance.original_settings = settings_serializer(instance.settings).data

        # Save instance
        instance.save()

    def save(self, **kwargs):
        instance: "Invoice" = super().save(**kwargs)

        # Set details originals
        for detail in instance.details.all():
            InvoiceDetailSerializer(detail).set_originals()

        # Set payments originals
        for payment in instance.payments.all():
            InvoicePaymentSerializer(payment).set_originals()

        # Set self originals
        self.set_originals(instance)

        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['sale_condition'] = data.pop("original_sale_condition")
        data['contact_address'] = data.pop("original_address")
        data['contact'] = data.pop("original_contact")
        data['settings'] = data.pop("original_settings")
        data['user'] = data.pop("original_user")
        data['sales_point'] = data.pop("original_sales_point")
        return data

    class Meta:
        model = Invoice
        fields = '__all__'
        extra_kwargs = {
            'number': {'required': False},
            'numeration': {'required': False},
            'sale_condition_name': {'required': False},
            'user': {'required': False},
            'settings': {'required': False},
        }
