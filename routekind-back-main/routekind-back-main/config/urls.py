"""Main URLs module."""

from django.conf import settings
from django.urls import path, include, re_path
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API DOC for Kind back",
        default_version='v0.1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    # re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # path('api/documentation', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # Django Admin... 
    path('api/' + settings.ADMIN_URL, admin.site.urls),
    # Custom urls
    path('profile/', include('kind.customauth.urls.profile_url')),
    path('users/', include('kind.customauth.urls.users_url')),
    path('auth/', include('kind.customauth.urls.auth_urls')),
    path('companies/', include('kind.companies.urls')),
    path('contacts/', include('kind.contacts.urls')),
    path('addresses/', include('kind.addresses.urls')),
    path('orders/', include('kind.orders.urls')),
    path('inventory/', include('kind.inventory.urls')),
    path('sales/', include('kind.sales.urls')),
    path('tasks/', include('kind.tasks.urls')),
    path('zones/', include('kind.zones.urls')),
    path('audits/', include('kind.useraudit.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
