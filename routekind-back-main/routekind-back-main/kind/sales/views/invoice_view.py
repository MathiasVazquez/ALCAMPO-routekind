
from typing import TYPE_CHECKING
from datetime import datetime

from django.http import HttpRequest
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import serializers

from kind.sales.serializers import InvoiceSerializer
from kind.generics.views.base_view import BaseModelViewSet
from kind.tasks.models.task_model import Task

if TYPE_CHECKING:
    from kind.sales.models import Invoice


class InvoiceView(BaseModelViewSet):
    serializer_class = InvoiceSerializer

    @action(methods=["post"], detail=True)
    def cancel(self, request, pk=None):
        invoice: 'Invoice' = self.get_object()
        if invoice.canceled:
            raise ValidationError({"error": "This invoice is already canceled."})

        data: dict = request.data

        invoice.canceled_datetime = datetime.now()
        invoice.canceled_coords = data.get('coords', None)
        invoice.canceled_by = request.user
        invoice.canceled = True
        invoice.save()

        return Response()
