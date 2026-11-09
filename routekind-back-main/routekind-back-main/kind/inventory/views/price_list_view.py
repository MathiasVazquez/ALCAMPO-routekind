from typing import TYPE_CHECKING
from kind.companies.models.inventory_settings import USER_PRICE_LIST_SOURCE

from kind.inventory.serializers import PriceListSerializer
from kind.generics.views.base_view import BaseModelViewSet

if TYPE_CHECKING:
    from kind.customauth.models import User


class PriceListView(BaseModelViewSet):
    serializer_class = PriceListSerializer

    def get_queryset(self):
        user: 'User' = self.request.user

        if user.company.price_list_source == USER_PRICE_LIST_SOURCE:
            return user.assigned_sales_point.price_lists

        return super().get_queryset()
