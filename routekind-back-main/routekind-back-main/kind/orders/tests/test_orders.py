
from datetime import datetime

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.exceptions import ValidationError

from kind.customauth.models import User
from kind.orders.models import Order
from kind.addresses.models import Address
from kind.contacts.models import Contact
from kind.inventory.models import SalesPoint
from kind.sales.models.invoice_model import Invoice
from kind.sales.models.invoice_setting_model import InvoiceSetting
from kind.tasks.models.task_model import Task, TaskStatus


class OrdersTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user: 'User' = User.objects.create_superuser(
            'admin',
            'admin@example.com',
            'admin'
        )
        self.client.force_authenticate(user=self.admin_user)
        # Set test company
        self.company = self.admin_user.company
        # Set test address
        self.contact_address = Address.objects.create(
            description='Home',
            coords={"latlng": [-25.35387253299717, -57.59847571302308]},
            company=self.company,
        )
        # Set test contact
        self.contact = Contact.objects.create(
            first_name="Luis",
            last_name="Meza",
            document="123456",
            company=self.company,
        )
        self.contact.addresses.add(self.contact_address)
        # Set test sales point
        self.sales_point = SalesPoint.objects.create(
            name='SP1',
            company=self.company,
        )
        self.admin_user.assigned_sales_point = self.sales_point
        self.admin_user.save()
        # Set test invoice settings
        self.invoice_setting = InvoiceSetting.objects.create(
            number="1512512",
            enumeration_prefix="001-001-",
            enumeration_postfix="",
            start_date="2023-04-04",
            due_date="2024-04-04",
            sales_point=self.sales_point,
            enumeration_pad_length=10,
            company=self.company,
        )

    def test_create_order(self):
        order1: Order = Order.objects.create(
            order_number="1",
            sales_point=self.sales_point,
            description='None',
            contact_address=self.contact_address,
            company=self.company,
        )
        task: 'Task' = order1.tasks.first()

        self.assertEqual(order1.order_number, "1")
        self.assertEqual(order1.tasks.count(), 1)
        self.assertEqual(task.current_status.name, "pending")
        self.assertEqual(task.status_logs.count(), 1)

        # Set next task status
        task.current_status = TaskStatus(
            name="finished",
        )
        task.save()
        self.assertEqual(task.status_logs.count(), 2)
        self.assertEqual(task.current_status.name, "finished")

        # Set invalid next task status
        with self.assertRaises(ValidationError):
            task.current_status = TaskStatus(
                name="cancellll",
            )
            task.save()

        with self.assertRaises(ValidationError):
            task.current_status = TaskStatus(
                name="cancel",
            )
            task.save()

    def test_invoice_order(self):
        # Order2
        order2: Order = Order.objects.create(
            order_number="2",
            sales_point=self.sales_point,
            description='Entrega',
            contact_address=self.contact_address,
            company=self.company,
        )

        # Order2 to invoice
        new_invoice = Invoice(
            user=self.admin_user,
            order=order2,
            numeration=self.invoice_setting.formated_next_auto_enumeration,
            number=self.invoice_setting.number,
            datetime=datetime.now(),
            settings=self.invoice_setting,
            company=self.company,
        )
        new_invoice.save()

        # Check order2 new status after invoicing
        order_task: 'Task' = order2.tasks.last()
        self.assertEqual(order_task.current_status.name, 'finished')

        # Check order2's invoice status after creating
        invoice_task: 'Task' = order2.invoice.tasks.last()
        self.assertEqual(invoice_task.current_status.name, 'created')
