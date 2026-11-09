
from kind.inventory.serializers import WarehouseSerializer
from kind.generics.views.base_view import BaseModelViewSet


class WarehouseView(BaseModelViewSet):
    serializer_class = WarehouseSerializer
