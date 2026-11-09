from django.contrib import admin
from kind.orders.models import Order, OrderDetail, OrderPayment


@admin.register(OrderPayment)
class OrderPaymentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'amount',
        'confirmed',
        'order',
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order_number',
        'sales_point',
        'start_date',
        'due_date',
    )


@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'quantity',
        'unit_price',
    )
