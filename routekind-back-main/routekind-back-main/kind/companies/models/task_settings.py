
from typing import TYPE_CHECKING

from django.db import models
from rest_framework.exceptions import ValidationError

if TYPE_CHECKING:
    from kind.tasks.models import TaskPriority, StatusFlowTemplate
    from kind.companies.models import Company


class CompanyTaskSettingsMixin(models.Model):
    default_task_priority: 'TaskPriority' = models.ForeignKey(
        'tasks.TaskPriority',
        blank=True,
        null=True,
        related_name='default_priority_at_companies',
        on_delete=models.SET_NULL,
    )

    default_on_create_address_task_template: 'StatusFlowTemplate' = models.ForeignKey(
        'tasks.StatusFlowTemplate',
        blank=True,
        null=True,
        related_name='default_on_create_address_task_template_at_companies',
        on_delete=models.SET_NULL,
    )

    def save(self, *args, **kwargs):
        if self.default_task_priority:
            task_company: 'Company' = self.default_task_priority.company
            if task_company.id != self.id:
                raise ValidationError({
                    'error': 'Cannot assign this task priority as default.'
                })

        return super().save(*args, **kwargs)

    class Meta:
        abstract = True
