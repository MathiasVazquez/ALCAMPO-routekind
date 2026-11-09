from kind.companies.serializers import CompanySerializer
from kind.companies.models import Company

from kind.generics.views import CustomView

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated


from functools import wraps
from django.core.exceptions import PermissionDenied


def user_has_permission(permission):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(view, *args, **kwargs):
            request = view.request
            user, method = request.user, request.method
            valid_conditions = [
                user.is_superuser,
                user.has_perm(f"{permission}.read") and method == 'GET',
                user.has_perm(f"{permission}.create") and method == 'POST',
                user.has_perm(f"{permission}.update") and method in ['PUT', 'PATCH'],
                user.has_perm(f"{permission}.delete") and method == 'DELETE',
            ]
            if any(valid_conditions):
                return view_func(view, *args, **kwargs)
            raise PermissionDenied
        return wrapper
    return decorator


class CompanyView(CustomView):
    serializer_class = CompanySerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        return Company.objects.all()

    def get_permissions(self):
        self.use_default_permissions = True
        return super().get_permissions()

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated,)
    )
    # @user_has_permission("company")
    def profile(self, request):
        company = request.user.company
        serializer = self.get_serializer(company, context={"request": request})
        return Response(serializer.data)
    