
from typing import TYPE_CHECKING, cast
from datetime import timedelta

from django.db.models import Q
from django.utils import timezone
from django.http import HttpRequest
from django.db.models import Manager, QuerySet
from django.db.models import OuterRef, Subquery, CharField, Max, Case, When, Value, IntegerField
from django.db.models.functions import Cast
from rest_framework.response import Response

from kind.customauth.models.user_model import User
from kind.generics.views.base_view import BaseModelViewSet
from kind.sales.models.invoice_model import Invoice
from kind.sales.serializers.invoice_serializer import InvoiceSerializer
from kind.tasks.serializers import TaskSerializer, StatusFlowTemplateSerializer
# from kind.addresses.serializers import AddressSerializer

from kind.orders.models import Order
from kind.orders.serializers import OrderSerializer


class StatusFlowTemplateView(BaseModelViewSet):
    serializer_class = StatusFlowTemplateSerializer

    def get_queryset(self) -> QuerySet:
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            return qs

        return qs.filter(admin_required=False)


class TaskView(BaseModelViewSet):
    serializer_class = TaskSerializer

    def get_permissions(self):
        if self.action == 'partial_update' and 'current_status' in self.request.data:
            self.custom_action = 'interact'
        return super().get_permissions()
