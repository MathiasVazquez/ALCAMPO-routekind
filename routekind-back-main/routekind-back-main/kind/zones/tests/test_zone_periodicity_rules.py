
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
from kind.zones.models import Zone, Polygon
# from kind.zones.serializers import ZoneSerializer


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
        # self.admin_user.assigned_sales_point = self.sales_point
        # self.admin_user.save()
        # Set test invoice settings
        # self.invoice_setting = InvoiceSetting.objects.create(
        #     number="1512512",
        #     enumeration_prefix="001-001-",
        #     enumeration_postfix="",
        #     start_date="2023-04-04",
        #     due_date="2024-04-04",
        #     sales_point=self.sales_point,
        #     enumeration_pad_length=10,
        #     company=self.company,
        # )

    def test_create_zone(self):
        zone = Zone.objects.create(
            label="Zone1",
            # users=[str(self.admin_user.id)],
            zone_periodicity_rules={
                "asociation": "and",
                "rules": [
                    {
                        "type": "ever",
                        "values": []
                    }
                ]
            },
            company=self.company,
        )
        zone.users.add(self.admin_user)

        polygons = Polygon.objects.create(
            zone=zone,
            vertices=[
                [-25.27249898238207, -57.60204328944955],
                [-25.277435385198167, -57.589103444000585],
                [-25.28273722378945, -57.60012253114073]
            ],
            company=self.company,
        )

        self.assertIsNotNone(zone)
        self.assertEqual(zone.polygons.count(), 1)
        self.assertEqual(len(zone.polygons.first().vertices), 3)

        # Check availability with rule 1
        self.assertTrue(zone.is_available_today)

        # Check availability with dates rule 1
        zone.zone_periodicity_rules = {
            "asociation": "and",
            "rules": [
                {
                    "type": "dates",
                    "values": ["2024-01-01", "2024-01-02"]
                }
            ]
        }
        self.assertFalse(zone.is_available_today)

        # Check availability with dates rule 2
        zone.zone_periodicity_rules = {
            "asociation": "and",
            "rules": [
                {
                    "type": "dates",
                    "values": ["2024-01-01", "2024-01-02", datetime.now().strftime("%Y-%m-%d")]
                }
            ]
        }
        self.assertTrue(zone.is_available_today)

        # Check availability with ranges rule 1
        zone.zone_periodicity_rules = {
            "asociation": "and",
            "rules": [
                {
                    "type": "ranges",
                    "values": [["2024-01-01", "2024-01-02"]]
                }
            ]
        }
        self.assertFalse(zone.is_available_today)

        # Check availability with ranges rule 2
        zone.zone_periodicity_rules = {
            "asociation": "and",
            "rules": [
                {
                    "type": "ranges",
                    "values": [
                        ["2024-01-01", "2024-01-02"],
                        ["2024-01-03", datetime.now().strftime("%Y-%m-%d")]
                    ]
                }
            ]
        }
        self.assertTrue(zone.is_available_today)

        # Check availability with weekdays rule 1
        zone.zone_periodicity_rules = {
            "asociation": "and",
            "rules": [
                {
                    "type": "weekdays",
                    "values": [1, 2, 4 if datetime.now().weekday() + 1 == 3 else 3]
                }
            ]
        }
        self.assertFalse(zone.is_available_today)

        # Check availability with weekdays rule 2
        zone.zone_periodicity_rules = {
            "asociation": "and",
            "rules": [
                {
                    "type": "weekdays",
                    "values": [datetime.now().weekday() + 1]
                }
            ]
        }
        self.assertTrue(zone.is_available_today)

        # Check availability with months rule 1
        zone.zone_periodicity_rules = {
            "asociation": "and",
            "rules": [
                {
                    "type": "months",
                    "values": [2 if datetime.now().month == 1 else 1]
                }
            ]
        }
        self.assertFalse(zone.is_available_today)

        # Check availability with months rule 2
        zone.zone_periodicity_rules = {
            "asociation": "and",
            "rules": [
                {
                    "type": "months",
                    "values": [datetime.now().month]
                }
            ]
        }
        self.assertTrue(zone.is_available_today)

        # Check availability with monthdays rule 1
        zone.zone_periodicity_rules = {
            "asociation": "and",
            "rules": [
                {
                    "type": "monthdays",
                    "values": [2 if datetime.now().timetuple().tm_yday == 1 else 1]
                }
            ]
        }
        self.assertFalse(zone.is_available_today)

        # Check availability with monthdays rule 2
        zone.zone_periodicity_rules = {
            "asociation": "and",
            "rules": [
                {
                    "type": "monthdays",
                    "values": [datetime.now().timetuple().tm_yday]
                }
            ]
        }
        self.assertTrue(zone.is_available_today)
