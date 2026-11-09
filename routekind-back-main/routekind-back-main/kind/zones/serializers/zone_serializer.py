
from rest_framework import serializers

from kind.useraudit.models.user_audit_model import UserAudit
from kind.zones.models import Zone
from kind.generics.serializers import BaseSerializer
from kind.customauth.models import User
from kind.addresses.models import Address
from .polygon_serializer import PolygonSerializer


class ZoneSerializer(BaseSerializer):
    polygons = PolygonSerializer(many=True, required=False)
    is_available_today = serializers.ReadOnlyField()
    # coords = serializers.ReadOnlyField()

    def create(self, validated_data: dict):
        zone: 'Zone' = super().create(validated_data)

        # Create audit register
        UserAudit.add_zones_log(
            zone,
            self.get_user(),
            self.ip_address,
            self.device_name,
            created=True
        )

        return zone

    def update(self, instance, validated_data):
        task: 'Zone' = super().update(instance, validated_data)

        # Audit update
        request_data: dict = self.context.get('request').data
        users: list = request_data.get('users', None)
        label: dict = request_data.get('label', None)
        excluded_addresses: dict = request_data.get('excluded_addresses', None)
        additional_addresses: dict = request_data.get('additional_addresses', None)

        if users is not None or label or excluded_addresses is not None or additional_addresses is not None:
            entry_status = {
                **({"users": list(User.objects.filter(id__in=users).values_list('username', flat=True))} if users is not None else {}),
                **({"excludedAddresses": list(Address.objects.filter(id__in=excluded_addresses).values_list('description', flat=True))} if excluded_addresses is not None else {}),
                **({"additionalAddresses": list(Address.objects.filter(id__in=additional_addresses).values_list('description', flat=True))} if additional_addresses is not None else {}),
                **({"label": label} if label else {}),
            }
            UserAudit.add_zones_log(
                task,
                self.get_user(),
                self.ip_address,
                self.device_name,
                entry_status=entry_status
            )

        return task

    class Meta:
        model = Zone
        fields = '__all__'
