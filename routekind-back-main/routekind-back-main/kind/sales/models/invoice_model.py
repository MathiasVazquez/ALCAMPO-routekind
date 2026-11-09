
from typing import TYPE_CHECKING

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from rest_framework.exceptions import ValidationError

from kind.addresses.models.address_model import Address
from kind.companies.models.company_model import Company
from kind.contacts.models.contact_model import Contact
from kind.custom_fields.coords_field import CoordsJSONField

from kind.generics.models.custom_transaction_model import CustomTransactionAbstract
from kind.tasks.models.task_model import StatusFlowTemplate, Task
from kind.transactions.models.transation_detail_model import TransactionDetailAbstract
from kind.transactions.models.transation_payment_model import TransactionPaymentAbstract
from kind.tasks.models import TaskStatus

if TYPE_CHECKING:
    from kind.orders.models import Order
    from kind.sales.models import InvoiceSetting
    from kind.inventory.models import SaleCondition
    from kind.customauth.models import User, SalesPoint
    from kind.inventory.models.warehouse_model import WarehouseProductDetail


class Invoice(CustomTransactionAbstract):
    numeration = models.CharField(max_length=120)
    number = models.CharField(max_length=120)
    coords = CoordsJSONField(default=None, null=True, blank=True)
    datetime = models.DateTimeField()
    original_user = models.JSONField(default=dict)
    user: "User" = models.ForeignKey(
        'customauth.User',
        null=True,
        blank=True,
        related_name="emited_invoices",
        on_delete=models.SET_NULL
    )
    original_sales_point = models.JSONField(default=dict)
    sales_point: "SalesPoint" = models.ForeignKey(
        'inventory.SalesPoint',
        null=True,
        blank=True,
        related_name="invoices",
        on_delete=models.SET_NULL
    )
    original_sale_condition = models.JSONField(default=dict)
    sale_condition: 'SaleCondition' = models.ForeignKey(
        'inventory.SaleCondition',
        null=True,
        blank=True,
        related_name="invoices",
        on_delete=models.SET_NULL
    )
    order: 'Order' = models.ForeignKey(
        'orders.Order',
        null=True,
        blank=True,
        related_name="invoices",
        on_delete=models.SET_NULL
    )
    original_settings = models.JSONField(default=dict)
    settings: 'InvoiceSetting' = models.ForeignKey(
        'sales.InvoiceSetting',
        related_name='invoices',
        on_delete=models.PROTECT,
    )
    details: models.Manager
    payments: models.Manager

    # Contact information
    original_address = models.JSONField(default=dict)
    contact_address: 'Address' = models.ForeignKey(
        'addresses.Address',
        related_name='invoices',
        on_delete=models.SET_NULL,
        null=True,
        default=None,
    )
    original_contact = models.JSONField(default=dict)
    contact: 'Contact' = models.ForeignKey(
        'contacts.Contact',
        related_name='invoices',
        on_delete=models.SET_NULL,
        null=True,
        default=None,
    )

    canceled = models.BooleanField(default=False)
    canceled_datetime = models.DateTimeField(null=True, blank=True, default=None)
    canceled_coords = CoordsJSONField(default=None, null=True, blank=True)
    canceled_by = models.ForeignKey(
        'customauth.User',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    # cancel_invoice_task: 'Task' = models.ForeignKey(
    #     'tasks.Task',
    #     related_name='canceled_invoices',
    #     on_delete=models.SET_NULL,
    #     blank=True,
    #     null=True,
    # )
    # @property
    # def canceled(self):
    #     return hasattr(self, 'cancel_invoice_task') and self.cancel_invoice_task is not None

    tasks: models.Manager

    def _on_create(self):
        # Set default settings (must go first)
        if not hasattr(self, "settings") or not self.settings:
            self.settings = self.user.assigned_sales_point.active_invoice_setting

        # Check numeration already exists
        if self.numeration and self.settings.invoices.filter(numeration=self.numeration).exists():
            raise ValidationError({
                "error": f"Invoice with numeration {self.numeration} already exist."
            })

        # Set default sales point
        if not self.sales_point:
            self.sales_point = self.user.assigned_sales_point

        # Set default number
        if not self.number:
            self.number = self.settings.number

        # Set default contact address from order
        if self.order:
            if not self.contact_address:
                self.contact_address = self.order.contact_address
            if not self.sale_condition:
                self.sale_condition = self.order.sale_condition

        # Validate address
        _contacts_from_address = Contact.objects.filter(
            addresses__id=self.contact_address.id
        )
        if not _contacts_from_address.exists():
            raise ValidationError({"error": "Invalid contact address."})
        if _contacts_from_address.count() > 1:
            # Never should happen...
            raise ValidationError({"error": "Contact must be defined for this address."})

        _contact_from_address = _contacts_from_address.first()
        if not self.contact:
            self.contact = _contact_from_address
        elif self.contact.id != _contact_from_address.id:
            raise ValidationError({"error": "Invalid contact address."})

        # Auto enumerate
        if self.settings.manage_auto_enumeration:
            self.numeration = self.settings.formated_next_auto_enumeration
            self.settings.autoenumerate()
        elif not self.numeration:
            raise ValidationError({"numeration": "This field is required."})

        # Check "throught" invoices
        throught_invoice_tasks = Task.objects.none()

        if self.order:
            throught_invoice_tasks |= self.order.tasks.all()

        if self.contact_address:
            throught_invoice_tasks |= self.contact_address.tasks.all()

        for task in throught_invoice_tasks:
            task: 'Task'
            for transition in task.current_status.transitions:
                throught = transition.get("throught")
                if throught == 'invoice':
                    task.current_status = TaskStatus(
                        name=transition.get("name")
                    )

        # Create invoice task
        company: 'Company' = self.company

        if not company.default_invoices_task_template:
            StatusFlowTemplate.create_default_invoices_template(company)

    def _create_invoice_task(self):
        company: 'Company' = self.company

        invoice_task = Task(
            subject=f"Factura Nro. {self.numeration}",
            description=""
            f"Entrega de factura Nro. {self.numeration} "
            f"a {self.contact.full_name} "
            f"en {self.contact_address.coords.get('address')}",
            contact_address=self.contact_address,
            invoice=self,
            order=self.order,
            company=company,
            created_by=self.created_by,
            updated_by=self.updated_by,
            flow=company.default_invoices_task_template,
        )
        invoice_task.users.add(self.created_by)
        invoice_task.sales_points.add(self.created_by.assigned_sales_point)
        invoice_task.save()
        # status_log: 'TaskStatus' = task.status_logs.first()
        # status_log.is_final = True
        # status_log.save()

    def _on_cancel(self):
        for detail in self.details.all():
            detail: "InvoiceDetail"
            detail.restore_stock()

        for task in self.tasks.all():
            task: 'Task'
            for transition in task.current_status.transitions:
                throught = transition.get("throught")
                if throught == 'invoice_cancel':
                    task.current_status = TaskStatus(
                        name=transition.get("name")
                    )

    def save(self, *args, **kwargs):
        is_adding = self._state.adding

        if is_adding:
            self._on_create()
        else:
            is_originally_canceled = self.__class__.objects.get(id=self.id).canceled
            if not is_originally_canceled and self.canceled:
                self._on_cancel()

        super().save(*args, **kwargs)

        if is_adding:
            self._create_invoice_task()


class InvoiceDetail(TransactionDetailAbstract):
    invoice: 'Invoice' = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name="details"
    )
    original_product = models.JSONField(default=dict)

    class Meta:
        verbose_name = 'Invoice detail'
        verbose_name_plural = 'Invoice details'

    def __str__(self):
        return f'Detail for invoice with number {self.invoice.numeration}'

    @property
    def warehouse_detail(self) -> "WarehouseProductDetail":
        warehouse = self.invoice.sales_point.warehouse
        return warehouse.details.filter(product__id=self.product.id).first()

    def discount_stock(self):
        warehouse_detail = self.warehouse_detail
        if warehouse_detail:
            warehouse_detail.available_quantity -= self.quantity
            warehouse_detail.save()

    def restore_stock(self):
        warehouse_detail = self.warehouse_detail
        if warehouse_detail:
            warehouse_detail.available_quantity += self.quantity
            warehouse_detail.save()

    def save(self, *args, **kwargs):
        if self.product.track_inventory:
            if self._state.adding:
                self.discount_stock()
            else:
                # TODO: Adjust stick on update (never should happen...)
                pass

        return super().save(*args, **kwargs)


@receiver(post_delete, sender=InvoiceDetail)
def modelo_eliminado(sender, instance: "InvoiceDetail", **kwargs):
    instance.restore_stock()


class InvoicePayment(TransactionPaymentAbstract):
    invoice: 'Invoice' = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name="payments"
    )
    original_method = models.JSONField(default=dict)

    def method_name(self):
        return self.original_method.get("name")

    class Meta:
        verbose_name = 'Invoice payment'
        verbose_name_plural = 'Invoice payments'

    def __str__(self):
        return f'{self.method.name} payment for invoice with numeration {self.invoice.numeration}'
