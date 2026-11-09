from rest_framework import serializers
from kind.useraudit.models import UserAudit


class UserAuditSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAudit
        fields = '__all__'
