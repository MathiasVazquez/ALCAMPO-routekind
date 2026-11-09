
from typing import TYPE_CHECKING

from django.http import HttpRequest
from rest_framework import serializers

from kind.useraudit.models.user_audit_model import UserAudit
from kind.zones.models import Polygon
from kind.generics.serializers import BaseSerializer
from kind.addresses.models import Address

if TYPE_CHECKING:
    from kind.customauth.models import User


class PolygonSerializer(BaseSerializer):
    addresses = serializers.SerializerMethodField()

    def get_addresses(self, instance: 'Polygon'):
        request: HttpRequest = self.context.get('request')
        user: 'User' = request.user
        if user.is_admin:
            return instance \
                .get_internal_addresses(Address.objects.filter(company=user.company)) \
                .values_list('id', flat=True)

        return []

        # TODO: Filter by:
        # - Is for today
        # - Group users?
        # - Is assigned polygon's zone?

    def create(self, validated_data: dict):
        polygon: 'Polygon' = super().create(validated_data)

        # Create audit register
        entry_log = f'{polygon.created_by.name} ({polygon.created_by.username}) ha añadido el polígono <{polygon.auto_id}> en la zona "{polygon.zone.label}".'
        UserAudit.add_zones_log(
            polygon.zone,
            self.get_user(),
            self.ip_address,
            self.device_name,
            entry_log=entry_log,
            entry_status={
                "polygons": list(polygon.zone.polygons.values_list("auto_id", flat=True)),
            }
        )

        return polygon

    def update(self, instance: 'Polygon', validated_data):
        polygon: 'Polygon' = super().update(instance, validated_data)
        user = self.get_user()
        ip_address = self.ip_address
        device_name = self.device_name

        request_data: dict = self.context.get('request').data

        # Label updated
        label: str = request_data.get('label', None)
        if label is not None:
            entry_log = f'{user.name} (@{user.username}) ha modificado el nombre del polígono <{polygon.auto_id}> de la zona "{polygon.zone.label}"'
            UserAudit.add_zones_log(
                polygon.zone,
                self.get_user(),
                ip_address,
                device_name,
                entry_log=entry_log,
                entry_status={
                    "label": label,
                }
            )

        # Vertices updated
        vertices: list = request_data.get('vertices', None)
        if vertices is not None:
            entry_log = f'{user.name} (@{user.username}) ha modificado el polígono {polygon.label} <{polygon.auto_id}> de la zona "{polygon.zone.label}"'
            UserAudit.add_zones_log(
                polygon.zone,
                self.get_user(),
                ip_address,
                device_name,
                entry_log=entry_log,
                entry_status={
                    "vertices": f"{len(vertices)}",
                }
            )

        return polygon

    class Meta:
        model = Polygon
        fields = '__all__'
