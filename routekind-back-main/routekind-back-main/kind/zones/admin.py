from django.contrib import admin
from kind.zones.models import Zone, Polygon


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'label',
    )


@admin.register(Polygon)
class PolygonAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'zone',
    )
