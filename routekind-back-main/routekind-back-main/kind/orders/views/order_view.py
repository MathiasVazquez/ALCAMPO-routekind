
from typing import TYPE_CHECKING
from datetime import datetime

from django.db import transaction
from django.http import HttpRequest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from kind.companies.models.company_model import Company

from kind.orders.serializers import OrderSerializer
from kind.generics.views.base_view import BaseModelViewSet
from kind.sales.models.invoice_model import Invoice, InvoiceDetail, InvoicePayment
from kind.sales.serializers import InvoiceSerializer

if TYPE_CHECKING:
    from kind.customauth.models import User
    from kind.orders.models import Order


class OrderView(BaseModelViewSet):
    serializer_class = OrderSerializer

    @transaction.atomic
    @action(methods=["post"], detail=True)
    def to_invoice(self, request: HttpRequest, pk=None):
        # Check order is already invoiced
        order: 'Order' = self.get_object()
        if order.is_invoiced:
            raise ValidationError({
                "error": f"Order with number '{order.order_number}' is already invoiced ({order.invoice.numeration})."
            })

        # Check partial payment
        user: 'User' = self.request.user
        # if not user.company.allow_partial_payment and order.is_partial:
        #     raise ValidationError({
        #         "error": f"Order with number '{order.order_number}' have partial payments."
        #     })

        # Create new invoice
        invoice_setting = user.assigned_sales_point.active_invoice_setting
        # invoice_data = {
        #     "order": order.id,
        #     "numeration": invoice_setting.formated_next_auto_enumeration,
        #     "number": invoice_setting.number,
        #     "date": datetime.now().date(),
        #     "settings": invoice_setting.id,
        # }
        # invoice_serializer = InvoiceSerializer(data=invoice_data, context={"request": request})
        # invoice_serializer.is_valid(raise_exception=True)
        # invoice_serializer.save()
        # new_invoice = None
        new_invoice = Invoice(
            user=user,
            order=order,
            numeration=invoice_setting.formated_next_auto_enumeration,
            number=invoice_setting.number,
            datetime=datetime.now(),
            settings=invoice_setting,
            company=user.company,
        )

        new_invoice.save()

        # Create product details
        if not request.data.get("details"):
            for [quantity, unit_price, product_id] in order.details.values_list(
                'quantity',
                'unit_price',
                'product_id'
            ):
                InvoiceDetail.objects.create(
                    invoice=new_invoice,
                    quantity=quantity,
                    unit_price=unit_price,
                    company=user.company,
                    product_id=product_id,
                )

        # Create payments
        if not request.data.get("details"):
            for [amount, method_id] in order.payments.values_list(
                'amount',
                'method_id'
            ):
                InvoicePayment.objects.create(
                    invoice=new_invoice,
                    amount=amount,
                    company=user.company,
                    method_id=method_id,
                )

        # Update with request changes
        if request.data is not None:
            invoice_update_serializer = InvoiceSerializer(
                new_invoice,
                partial=True,
                data=request.data,
                context={"request": request},
            )
            invoice_update_serializer.is_valid(raise_exception=True)
            invoice_update_serializer.save()

        # Check "allow_partial_payment"
        company: 'Company' = user.company
        if not company.allow_partial_payment and new_invoice.is_partial:
            raise ValidationError({
                "error": "Cannot create an invoice from an order with partial payments."
            })

        serializer = InvoiceSerializer(new_invoice)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
