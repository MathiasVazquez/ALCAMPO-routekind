from django.contrib import admin
from kind.inventory.models import (
    Warehouse,
    Batch,
    Measurement,
    PriceList,
    PriceListDetail,
    Product,
    Tax,
    MoneyType,
    WarehouseProductDetail,
    SaleCondition,
    SalePayment,
    PaymentMethod,
    SalesPoint,
)


@admin.register(SalePayment)
class SalePaymentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'method',
        'amount',
        'confirmed',
    )


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'code',
    )


@admin.register(SaleCondition)
class SaleConditionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'code',
    )


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )


@admin.register(WarehouseProductDetail)
class WarehouseProductDetailAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'warehouse',
        'product',
        'available_quantity',
    )


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'code',
        'product',
        'warehouse',
        'quantity',
    )


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )


@admin.register(PriceList)
class PriceListAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )


@admin.register(PriceListDetail)
class PriceListDetailAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'product',
        'price_list',
        'unit_price',
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'track_batches',
        'track_inventory',
    )


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'percentage',
    )


@admin.register(MoneyType)
class MoneyTypeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'code',
    )


@admin.register(SalesPoint)
class SalesPointAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'active_invoice_setting')
