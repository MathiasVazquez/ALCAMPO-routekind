from django.contrib import admin
from kind.addresses.models import Address


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'description',
        'company',
    )
