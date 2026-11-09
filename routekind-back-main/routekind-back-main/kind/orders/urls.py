from rest_framework.routers import DefaultRouter

from .views import OrderView


router = DefaultRouter()

router.register('', OrderView, basename='orders')

urlpatterns = router.urls
