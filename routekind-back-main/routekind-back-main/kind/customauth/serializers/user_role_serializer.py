
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from kind.customauth.models import UserRole
from kind.generics.serializers.base_seriaizer import BaseSerializer


class UserRoleSerializer(BaseSerializer):

    class Meta:
        fields = [
            'id',
            'name',
            'description',
            'permissions',
        ]
        model = UserRole
