from rest_framework.routers import DefaultRouter

from .views import (
    PriceListView,
    ProductView,
    SaleConditionView,
    PaymentMethodView,
    SalePaymentView,
    SalesPointView,
    WarehouseView,
    MeasureUnitView,
)


router = DefaultRouter()

router.register('unit-measurements', MeasureUnitView, basename='unit-measurements')
router.register('price-lists', PriceListView, basename='price-lists')
router.register('products', ProductView, basename='products')
router.register('warehouses', WarehouseView, basename='warehouses')

# payments

router.register('payments/methods', PaymentMethodView, basename='payment-methods')
router.register('sales/conditions', SaleConditionView, basename='sale-conditions')
router.register('sales/payments', SalePaymentView, basename='sale-payments')

# Sales point
router.register('salespoints', SalesPointView, basename='salespoints')


urlpatterns = router.urls
