from rest_framework.routers import DefaultRouter

from .views import CompanyView

router = DefaultRouter()

router.register('', CompanyView, basename='companies')

urlpatterns = router.urls
