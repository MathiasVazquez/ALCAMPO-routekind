from kind.customauth.views import UserView

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('', UserView, basename='users')

urlpatterns = router.urls
