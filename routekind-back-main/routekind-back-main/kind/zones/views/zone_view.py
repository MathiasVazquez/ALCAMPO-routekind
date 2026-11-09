from django.http import HttpRequest

from typing import TYPE_CHECKING

# from django import
from rest_framework import serializers

from kind.useraudit.models.user_audit_model import UserAudit
from kind.zones.serializers import ZoneSerializer, PolygonSerializer
from kind.generics.views.base_view import BaseModelViewSet

if TYPE_CHECKING:
    from kind.customauth.models import User
    from kind.zones.models import Polygon, Zone


class ZoneView(BaseModelViewSet):

    serializer_class = ZoneSerializer

    def get_queryset(self):
        user: 'User' = self.request.user
        qs = super().get_queryset()

        if (
            user.is_superuser or
            user.has_permission('zones.update') or
            user.has_permission('zones.create') or
            user.has_permission('zones.delete')
        ):
            return qs

        today_zones_ids = [
            zone.id
            for zone
            in qs.filter(users__id=user.id)
            if zone.is_available_today
        ]
        return qs.filter(id__in=today_zones_ids)

    def destroy(self, request: HttpRequest, *args, **kwargs):
        zone: 'Zone' = self.get_object()

        # Audit
        ip_address = request.META.get('REMOTE_ADDR')
        device_name = request.headers.get("Device", None)
        entry_log = f'{request.user.name} ({request.user.username}) ha eliminado la zona {zone.label}'
        UserAudit.add_zones_log(
            zone,
            request.user,
            ip_address,
            device_name,
            entry_log=entry_log,
            entry_status={},
            deleted=True
        )

        return super().destroy(request, *args, **kwargs)


class PolygonView(BaseModelViewSet):
    serializer_class = PolygonSerializer

    class SetAtCoordsSerializer(serializers.Serializer):
        zone_type = serializers.CharField(max_length=60)
        latlng = serializers.JSONField()

    def destroy(self, request: HttpRequest, *args, **kwargs):
        polygon: 'Polygon' = self.get_object()
        user: 'User' = request.user

        # Audit
        entry_log = f'{user.name} ({user.username}) ha removido el polígono <{polygon.auto_id}> de la zona "{polygon.zone.label}"'
        ip_address = request.META.get('REMOTE_ADDR')
        device_name = request.headers.get("Device", None)
        UserAudit.add_zones_log(
            polygon.zone,
            user,
            ip_address,
            device_name,
            entry_log=entry_log,
            entry_status={}
        )

        return super().destroy(request, *args, **kwargs)
