from rest_framework import serializers
from kind.generics.serializers import BaseSerializer
from kind.addresses.models import Address
from kind.contacts.models import Contact
from kind.useraudit.models import UserAudit


class FlatContactSerializer(BaseSerializer):
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Contact
        fields = '__all__'


class AddressSerializer(BaseSerializer):
    # tasks = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    contact = FlatContactSerializer(allow_null=True, required=False)
    tasks = serializers.SerializerMethodField()

    def get_tasks(self, instance: 'Address'):
        return [str(id) for id in instance.tasks.values_list('id', flat=True)]

    def create(self, validated_data: dict):
        user = self.get_user()

        # Create address
        address: 'Address' = super().create(validated_data)
        address.refresh_from_db()
        UserAudit.add_create_addresses_log(address, user, self.ip_address, self.device_name)

        # Create task
        task = address.create_first_task()
        UserAudit.add_tasks_log(task, user, self.ip_address, self.device_name, created=True)

        return address

    class Meta:
        model = Address
        fields = '__all__'
