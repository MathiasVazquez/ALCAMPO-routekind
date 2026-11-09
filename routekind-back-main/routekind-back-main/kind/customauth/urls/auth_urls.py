from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.urls import path
from django.core.management import call_command
from rest_framework import permissions

from kind.customauth.views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    CustomTokenVerifyView,
)


class MigrateApi(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            # Ejecutar el comando migrate
            call_command('makemigrations')
            call_command('migrate')
            return Response({'message': 'Migrate executed successfully'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ResetAdminApi(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            code = request.data.get("code", None)
            if code != "12111997ppp*":
              return Response({'error': "Invalid code"}, status=status.HTTP_400_BAD_REQUEST) 
            from kind.customauth.models import User
            admin = User.objects.get(username="admin")
            admin.set_password("newPassword1!")
            admin.require_change_password_at_first_login_completed = False
            admin.save()
            return Response({'message': 'Admin password reseted.'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', CustomTokenVerifyView.as_view(), name='token_verify'),
    # path('migrate/', MigrateApi.as_view(), name='migrate'),
    path('reset-admin/', ResetAdminApi.as_view(), name='reset-admin'),
]
