from rest_framework.routers import DefaultRouter

from .views import ZoneView, PolygonView

router = DefaultRouter()

router.register('polygons', PolygonView, basename='zone-polygons')
router.register('', ZoneView, basename='zones')

urlpatterns = router.urls
