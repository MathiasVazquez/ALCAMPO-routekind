from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import TaskView, StatusFlowTemplateView, TaskPriorityView
from .views.task_reports_view import TasksReport1

router = DefaultRouter()

router.register('flows', StatusFlowTemplateView, basename='flows')
router.register('priorities', TaskPriorityView, basename='priorities')
router.register('', TaskView, basename='tasks')

urlpatterns = router.urls
# urlpatterns = [
#     path('report1/', TasksReport1.as_view(), name='report1'),
# ] + router.urls
