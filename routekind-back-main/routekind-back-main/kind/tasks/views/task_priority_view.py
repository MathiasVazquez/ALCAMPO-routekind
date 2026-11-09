
from kind.generics.views.base_view import BaseModelViewSet
from kind.tasks.serializers import TaskPrioritySerializer


class TaskPriorityView(BaseModelViewSet):
    serializer_class = TaskPrioritySerializer
