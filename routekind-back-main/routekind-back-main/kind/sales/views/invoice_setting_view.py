from kind.sales.serializers import InvoiceSettingSerializer
from kind.generics.views.base_view import BaseModelViewSet


class InvoiceSettingView(BaseModelViewSet):
    serializer_class = InvoiceSettingSerializer
