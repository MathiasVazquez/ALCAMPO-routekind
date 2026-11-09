from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from kind.customauth.models import User
from kind.customauth.models.temporal_password_model import TemporalPassword
from kind.customauth.serializers.temporal_password_serializer import TemporalPasswordSerializer
from kind.customauth.utils.crypt import decrypt_password
from kind.inventory.serializers import SalesPointSerializer
from kind.generics.serializers.base_seriaizer import BaseSerializer
from kind.useraudit.models.user_audit_model import UserAudit


class UserSerializer(BaseSerializer):
    # permissions = serializers.ReadOnlyField(label='Permisos')
    password = serializers.CharField(write_only=True, label='Contraseña')
    assigned_sales_point = SalesPointSerializer(required=False, allow_null=True, many=False)
    required_change_password = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()
    temporal_password_requests = serializers.SerializerMethodField()

    def get_temporal_password_requests(self, instance: 'User'):
        user: 'User' = self.context.get('request').user
        has_permission = user.has_permission('users.update')
        if not has_permission or instance.id != user.id:
            return []

        valid_users_ids = user.filter_users_by_restricted_roles(User.objects.filter(
            company=user.company,
            is_active=True
        )).values_list('id', flat=True)

        # Get temporal passwords
        temporal_password_qs = TemporalPassword.objects.filter(
            company=user.company,
            approved_by__isnull=True,
            user__in=valid_users_ids
        )

        # Serialize temporal passwords
        results = TemporalPasswordSerializer(
            temporal_password_qs,
            many=True,
            context=self.context
        ).data
        return results

    def get_permissions(self, instance: 'User'):
        list_of_permissions = instance.roles.values_list('permissions', flat=True)
        return list(set([item for sublist in list_of_permissions for item in sublist]))

    def get_required_change_password(self, instance: 'User'):
        return (
            instance.company.require_change_password_at_first_login and
            not instance.require_change_password_at_first_login_completed
        )

    def create(self, validated_data: dict):
        # Validate and decrypt password
        password = validated_data.get("password")
        if not password:
            raise ValidationError({"password": "This field is required"})

        validated_data = {
            **validated_data,
            "password": decrypt_password(password)
        }

        # Get user instance
        request_user: 'User' = self.context.get('request').user
        validated_data['company'] = request_user.company
        instance: 'User' = super().create(validated_data)

        # Create temporal password
        instance.create_temporal_password_request().approve(
            validated_data.get("password"),
            request_user
        )

        # User creste audit
        UserAudit.add_users_log(
            instance,
            self.get_user(),
            self.ip_address,
            self.device_name,
            created=True
        )

        return instance

    def update(self, instance: 'User', validated_data: dict):
        validated_data.pop('password', None)
        user: 'User' = super().update(instance, validated_data)
        ip_address = self.ip_address
        device_name = self.device_name

        # AUDIT USER (name)
        name = validated_data.get('name', None)
        if name is not None:
            UserAudit.add_users_log(
                instance,
                self.get_user(),
                ip_address,
                device_name,
                entry_status={
                    "name": name
                }
            )

        # AUDIT USER (email)
        email = validated_data.get('email', None)
        if email is not None:
            UserAudit.add_users_log(
                instance,
                self.get_user(),
                ip_address,
                device_name,
                entry_status={
                    "email": email
                }
            )

        # AUDIT USER (is_active)
        is_active = validated_data.get('is_active', None)
        if is_active is not None:
            UserAudit.add_users_log(
                instance,
                self.get_user(),
                ip_address,
                device_name,
                entry_status={
                    "isActive": is_active
                }
            )

        return user

    class Meta:
        fields = [
            'id',
            'assigned_sales_point',
            'username',
            'password',
            'email',
            'is_superuser',
            'name',
            'is_active',
            'track_coords',
            'coords',
            # 'coords_history',
            'required_change_password',
            'roles',
            'permissions',
            'last_activity_date',
            'temporal_password_requests',
        ]
        model = User
