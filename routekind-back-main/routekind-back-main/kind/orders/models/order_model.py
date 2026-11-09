from typing import TYPE_CHECKING
from datetime import datetime

from django.db import models
from rest_framework.exceptions import ValidationError

from kind.companies.models.company_model import Company
from kind.contacts.models.contact_model import Contact
from kind.generics.models.custom_transaction_model import CustomTransactionAbstract
from kind.sales.models.invoice_model import InvoiceDetail, InvoicePayment
from kind.tasks.models.task_model import StatusFlowTemplate, Task
from kind.transactions.models.transation_detail_model import TransactionDetailAbstract
from kind.transactions.models.transation_payment_model import TransactionPaymentAbstract

if TYPE_CHECKING:
    from kind.customauth.models.sales_point_model import SalesPoint
    from kind.addresses.models import Address
    from kind.customauth.models import User
    from kind.sales.models import Invoice


# SALES INFO:
# - sale_condition (contado/credito)
# - invoice_number

# - payments: {
#     payment_type (efectivo, ...)
#     amount
#     confirmed/checked (pagado o no pagado)
#     date
# }


class Order(CustomTransactionAbstract):
    order_number = models.CharField(max_length=1023, null=True, blank=True)
    contact_address: 'Address' = models.ForeignKey(
        'addresses.Address',
        on_delete=models.CASCADE
    )
    sales_point: 'SalesPoint' = models.ForeignKey(
        'inventory.SalesPoint',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='assigned_orders'
    )
    price_list = models.ForeignKey(
        "inventory.PriceList",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="orders",
    )
    sale_condition = models.ForeignKey(
        "inventory.SaleCondition",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="orders",
    )
    description = models.CharField(max_length=2040, blank=True, default='')
    start_date = models.DateTimeField(default=None, null=True, blank=True)
    due_date = models.DateTimeField(default=None, null=True, blank=True)
    invoices: models.Manager
    tasks: models.Manager

    @property
    def contact(self) -> Contact:
        return Contact.objects.filter(addresses__id=self.contact_address.id).first()

    @property
    def invoice(self) -> 'Invoice':
        return self.invoices.filter(canceled=False).first()

    @property
    def canceled_invoices(self):
        return self.invoices.filter(canceled=True)

    @property
    def is_invoiced(self):
        return self.invoices.filter(canceled=False).exists()

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f'{self.order_number}'

    def _on_create(self):
        company: 'Company' = self.company
        if not company.default_orders_task_template:
            # Create default orders task flow template
            StatusFlowTemplate.create_default_orders_template(self.company)

        # Create task
        task = Task.objects.create(
            subject=f"Pedido Nro. {self.order_number}",
            description=f"Entrega del pedido Nro. {self.order_number} a {self.contact.full_name} en {self.contact_address.coords.get('address')}",
            # type="order",
            contact_address=self.contact_address,
            order=self,
            company=self.company,
            flow=company.default_orders_task_template,
            start_date=self.start_date,
            due_date=self.due_date,
        )
        task.sales_points.add(self.sales_point)
        task.save()

    def save(self, *args, **kwargs):

        if self._state.adding:
            self._on_create()

        return super().save(*args, **kwargs)


class OrderDetail(TransactionDetailAbstract):
    order: 'Order' = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="details"
    )

    class Meta:
        verbose_name = 'Order detail'
        verbose_name_plural = 'Order details'

    def __str__(self):
        return f'Detail for order with number {self.order.order_number}'
        # return f'({self.id}) For order {self.order.id if self.order else "None"} with Product ({self.product.id if self.product else "None"}) product_name: {self.product.product_name}'


class OrderPayment(TransactionPaymentAbstract):
    order: 'Order' = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    class Meta:
        verbose_name = 'Order payment'
        verbose_name_plural = 'Order payments'

    def __str__(self):
        return f'Payment for order with number {self.order.order_number}'
