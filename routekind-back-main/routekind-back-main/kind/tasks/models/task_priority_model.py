
from django.db import models

from kind.generics.models import CustomModelAbstract
from kind.generics.models.named_model import StrictNamedModelMixin


class TaskPriority(CustomModelAbstract, StrictNamedModelMixin):
    label = models.CharField(max_length=120)
    color = models.CharField(max_length=20, default='grey')
    tasks: models.Manager

    def __str__(self):
        return self.label
