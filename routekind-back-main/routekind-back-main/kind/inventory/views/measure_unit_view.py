
from kind.inventory.serializers import MeasurementSerializer
from kind.generics.views.base_view import BaseModelViewSet


class MeasureUnitView(BaseModelViewSet):
    serializer_class = MeasurementSerializer
