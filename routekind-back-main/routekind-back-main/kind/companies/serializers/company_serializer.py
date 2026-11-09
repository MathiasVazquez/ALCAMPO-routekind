from typing import TYPE_CHECKING

from rest_framework import serializers

from kind.customauth.models import TemporalPassword
from kind.companies.models import Company
from kind.generics.serializers import BaseSerializer
from kind.inventory.serializers import MoneyTypeSerializer
from kind.customauth.models import UserRole
from kind.customauth.serializers import UserRoleSerializer, TemporalPasswordSerializer

if TYPE_CHECKING:
    from kind.customauth.models import User


class CompanySerializer(BaseSerializer):
    company = None
    default_money_type = MoneyTypeSerializer(many=False, required=False)
    allow_more_users = serializers.ReadOnlyField()
    active_users_count = serializers.ReadOnlyField()
    company_roles = serializers.SerializerMethodField()
    # temporal_password_requests = serializers.SerializerMethodField()

    # def get_temporal_password_requests(self, instance: 'Company'):
    #     user: 'User' = self.context.get('request').user
    #     if not user.is_superuser:
    #         return []

    #     temporal_password_qs = TemporalPassword.objects.filter(company=instance, approved_by__isnull=True)
    #     return TemporalPasswordSerializer(temporal_password_qs, many=True, context=self.context).data

    def get_company_roles(self, instance: 'Company'):
        request = self.context.get("request")
        user: "User" = request.user
        roles = None

        # Validate assigable roles to create new user
        if not user.is_superuser:
            roles = user.get_restricted_to_roles()
        
        # Get all roles
        if roles is None:
            roles = UserRole.objects.filter(company=instance)

        # name = "salesman"
        # role_filter = UserRole.objects.filter(name=name)
        # if not role_filter.exists():
        #     UserRole.objects.create(
        #         name=name,
        #         description="Vendedor",
        #         permissions=["addresses.all", "contacts.all", "tasks.all"],
        #         company=instance,
        #     )

        
        return UserRoleSerializer(roles, many=True, context=self.context).data

    class Meta:
        fields = "__all__"
        model = Company
