from rest_framework.routers import DefaultRouter

from .views import (
    InvoiceTemplateView,
    InvoiceSettingView,
    InvoiceView,
)


router = DefaultRouter()

router.register('invoices/templates', InvoiceTemplateView, basename='invoice-templates')
router.register('invoices/settings', InvoiceSettingView, basename='invoice-settings')
router.register('invoices', InvoiceView, basename='invoices')

urlpatterns = router.urls
