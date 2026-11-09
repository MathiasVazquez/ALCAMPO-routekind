from rest_framework.routers import DefaultRouter

from .views import ContactView

router = DefaultRouter()

router.register('', ContactView, basename='contacts')

urlpatterns = router.urls
