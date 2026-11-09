
from kind.tasks.models import TaskPriority
from kind.generics.serializers import BaseSerializer


class TaskPrioritySerializer(BaseSerializer):

    class Meta:
        model = TaskPriority
        fields = '__all__'
