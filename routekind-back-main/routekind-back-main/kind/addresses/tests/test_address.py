from django.test import TestCase
from rest_framework.test import APIClient

from kind.customauth.models import User
from kind.addresses.models import Address


class AddressTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            'admin',
            'admin@example.com',
            'admin'
        )
        self.client.force_authenticate(user=self.admin_user)
        # Set test company
        self.company = self.admin_user.company

    def test_create_address(self):
        latlng = [-25.35387253299717, -57.59847571302308]
        address1: Address = Address.objects.create(
            description='None',
            coords={"latlng": latlng},
            company=self.company,
        )
        address1.refresh_from_db()
        self.assertListEqual(address1.coords.get('latlng'), latlng)
        self.assertTrue(
            'raw' in address1.coords and
            isinstance(address1.coords.get('raw'), dict)
        )
        self.assertTrue(
            'address' in address1.coords and
            isinstance(address1.coords.get('address'), str)
        )
        self.assertTrue(
            'addressType' in address1.coords and
            isinstance(address1.coords.get('addressType'), str)
        )

    # def test_client_id(self):
    #     latlng = [-25.35387253299717, -57.59847571302308]
    #     address1: Address = Address.objects.create(
    #         description='None',
    #         coords={"latlng": latlng},
    #         company=self.company,
    #     )
