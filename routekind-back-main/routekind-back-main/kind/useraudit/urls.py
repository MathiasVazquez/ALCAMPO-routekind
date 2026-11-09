from rest_framework.routers import DefaultRouter

from .views import UserAuditView

router = DefaultRouter()

router.register('', UserAuditView, basename='user-audit')

urlpatterns = router.urls
