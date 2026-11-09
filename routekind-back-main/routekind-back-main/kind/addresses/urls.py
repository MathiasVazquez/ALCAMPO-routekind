from rest_framework.routers import DefaultRouter

from .views import AddressView


router = DefaultRouter()

router.register('', AddressView, basename='addresses')

urlpatterns = router.urls
