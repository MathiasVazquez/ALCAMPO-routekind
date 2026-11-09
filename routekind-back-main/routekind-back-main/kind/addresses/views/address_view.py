from django.http import HttpRequest
from kind.addresses.models.address_model import Address
from kind.addresses.serializers import AddressSerializer
from kind.generics.views.base_view import BaseModelViewSet
from kind.useraudit.models.user_audit_model import UserAudit


class AddressView(BaseModelViewSet):
    serializer_class = AddressSerializer
    # queryset = Address.objects.all()

    # def create(self, request: HttpRequest, *args, **kwargs):
    #     response = super().create(request, *args, **kwargs)

    #     # Create and audit task
    #     address_id = response.data.get("id")
    #     address = Address.objects.get(id=address_id)
    #     address.refresh_from_db()
    #     task = address.create_first_task()
    #     UserAudit.add_tasks_log(task, request.user, created=True)

    #     return response
