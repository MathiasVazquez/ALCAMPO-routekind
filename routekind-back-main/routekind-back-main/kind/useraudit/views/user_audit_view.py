from typing import TYPE_CHECKING

from django.db.models import QuerySet

from kind.generics.views.base_view import BaseModelViewSet
from kind.useraudit.serializers import UserAuditSerializer

if TYPE_CHECKING:
    from kind.customauth.models import User


class UserAuditView(BaseModelViewSet):
    serializer_class = UserAuditSerializer

    def get_queryset(self) -> QuerySet:
        # Limit registers (1000 by default)
        user: 'User' = self.request.user
        max_registers = user.company.max_get_audit_registers
        return super().get_queryset()[0:max_registers]
