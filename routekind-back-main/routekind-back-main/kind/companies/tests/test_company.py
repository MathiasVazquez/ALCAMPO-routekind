from django.test import TestCase
from rest_framework.test import APIClient

from kind.customauth.models import User


class CompanyTestCase(TestCase):
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
