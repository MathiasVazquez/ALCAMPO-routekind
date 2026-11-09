from kind.sales.serializers import InvoiceTemplateSerializer
from kind.generics.views.base_view import BaseModelViewSet


class InvoiceTemplateView(BaseModelViewSet):
    serializer_class = InvoiceTemplateSerializer
