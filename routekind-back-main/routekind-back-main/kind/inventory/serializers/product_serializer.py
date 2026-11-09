
from typing import TYPE_CHECKING

from django.db import models
from django.http import HttpRequest
from rest_framework import serializers

from kind.generics.serializers.base_seriaizer import BaseSerializer

from kind.inventory.models import Product, Measurement, Tax
from kind.inventory.models.warehouse_model import WarehouseProductDetail
from kind.inventory.serializers.warehouse_serializer import WarehouseProductDetailSerializer
from kind.utils import create_dynamic_fields_serializer

if TYPE_CHECKING:
    from kind.customauth.models import User


class MeasurementSerializer(BaseSerializer):

    class Meta:
        model = Measurement
        fields = '__all__'


class TaxSerializer(BaseSerializer):
    class Meta:
        model = Tax
        fields = '__all__'


class WarehouseDetailSerializer(WarehouseProductDetailSerializer):
    class Meta:
        model = WarehouseProductDetail
        fields = ["id", "available_quantity", "product"]


class ProductSerializer(BaseSerializer):
    taxes = create_dynamic_fields_serializer(
        TaxSerializer, ("id", "name", "percentage")
    )(required=False, many=True)
    unit_measurement = create_dynamic_fields_serializer(
        MeasurementSerializer, ("id", "name")
    )(required=False, many=False)
    warehouse_details = create_dynamic_fields_serializer(
        WarehouseProductDetailSerializer, ("id", "available_quantity", "warehouse")
    )(many=True, required=False)
    total_availability = serializers.SerializerMethodField()

    def get_total_availability(self, product: "Product"):
        # TODO: CHECK PERMISSIONS BEFORE RETURN ALL OR JUST FROM ASSIGNED WAREHOUSE...
        request: HttpRequest = self.context.get("request")
        user: "User" = request.user
        if not user.assigned_sales_point or not user.assigned_sales_point.warehouse:
            return 0
        return user.assigned_sales_point.warehouse.details \
            .filter(product=product) \
            .aggregate(
                total=models.Sum(models.F("available_quantity"))
            )['total']

    def to_representation(self, instance: 'Product'):
        data = super().to_representation(instance)

        if not instance.track_inventory:
            data.pop("warehouse_details", None)
            data.pop("total_availability", None)

        return data

    class Meta:
        model = Product
        fields = '__all__'
