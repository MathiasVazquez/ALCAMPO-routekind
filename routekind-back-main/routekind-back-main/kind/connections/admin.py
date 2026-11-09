from django.contrib import admin
from kind.connections.models import (
    ApiConnection,
    ApiConnectionModule,
    ApiConnectionModuleWebhook,
    ApiConnectionModuleWebhookResponse,
)


@admin.register(ApiConnection)
class ApiConnectionAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'label',
        'company',
    )


@admin.register(ApiConnectionModule)
class ApiConnectionModuleAdmin(admin.ModelAdmin):
    list_display = (
        'content_type',
        'connection',
        'company',
    )


@admin.register(ApiConnectionModuleWebhook)
class ApiConnectionModuleWebhookAdmin(admin.ModelAdmin):
    list_display = (
        'on_action',
        'method',
        'url',
        'connection_module',
        'company',
    )


@admin.register(ApiConnectionModuleWebhookResponse)
class ApiConnectionModuleWebhookResponseAdmin(admin.ModelAdmin):
    list_display = (
        'webhook',
        'created_at',
        'company',
    )
