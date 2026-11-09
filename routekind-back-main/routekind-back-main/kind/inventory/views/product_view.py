
from kind.inventory.serializers import ProductSerializer
from kind.generics.views.base_view import BaseModelViewSet


class ProductView(BaseModelViewSet):
    serializer_class = ProductSerializer
