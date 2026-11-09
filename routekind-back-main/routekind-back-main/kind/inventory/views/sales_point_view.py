
from typing import TYPE_CHECKING

from rest_framework.exceptions import ValidationError

from kind.inventory.serializers import SalesPointSerializer
from kind.generics.views.base_view import BaseModelViewSet

if TYPE_CHECKING:
    from kind.companies.models import Company


class SalesPointView(BaseModelViewSet):
    serializer_class = SalesPointSerializer

    def get_permissions(self):

        company: 'Company' = self.request.user.company
        if not company.enable_sales_points:
            raise ValidationError({'error': 'Sales points not enabled'})

        return super().get_permissions()
