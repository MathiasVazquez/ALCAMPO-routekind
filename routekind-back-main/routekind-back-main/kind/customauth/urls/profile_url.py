from django.urls import path

from kind.customauth.views import UserProfileView, ResetUserPasswordView, RequestAdminNewPassword

urlpatterns = [
    path('reset_password/', ResetUserPasswordView.as_view(), name='reset-user-password'),
    path('request_admin_password/', RequestAdminNewPassword.as_view(), name='request-admin-password'),
    path('', UserProfileView.as_view(), name='get-user-profile'),
]
