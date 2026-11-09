from django.contrib import admin
from kind.useraudit.models import UserAudit


@admin.register(UserAudit)
class UserAuditAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_by',
        'module_name',
        'ip_address',
        'device_info',
        'created_at',
    )
