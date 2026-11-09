from django.contrib import admin
from kind.sales.models import (
    InvoiceTemplate,
    InvoiceSetting,
    Invoice,
    InvoiceDetail,
    InvoicePayment,
)


@admin.register(InvoicePayment)
class InvoicePaymentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'amount',
        'confirmed',
        'invoice',
    )


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'numeration',
        'number',
        'datetime',
    )


@admin.register(InvoiceDetail)
class InvoiceDetailAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'invoice',
    )


@admin.register(InvoiceTemplate)
class InvoiceTemplateAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'is_active',
    )


@admin.register(InvoiceSetting)
class InvoiceSettingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'number',
        'start_date',
        'due_date',
    )
