from django.contrib import admin
from kind.customauth.models import (
    User,
    UserRole,
    AuthToken,
    TemporalPassword,
)


@admin.register(AuthToken)
class AuthTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'is_active')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'company', 'is_active')


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'is_active')


@admin.register(TemporalPassword)
class TemporalPasswordAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'approved_by', 'approved_date', 'expiry_date', 'complete_date')
