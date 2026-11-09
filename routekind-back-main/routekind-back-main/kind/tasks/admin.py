from django.contrib import admin
from kind.tasks.models import (
    Task,
    TaskStatus,
    StatusFlowTemplate,
    TaskPriority
)


@admin.register(StatusFlowTemplate)
class StatusFlowTemplateAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'label',
    )


@admin.register(TaskStatus)
class TaskStatusAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'label',
        'datetime',
        # 'is_final',
        'task',
    )


class TaskStatusInline(admin.TabularInline):
    model = TaskStatus
    extra = 1


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    inlines = [TaskStatusInline]
    list_display = (
        'id',
        'subject',
        'contact_address',
        'task_status_count'
    )

    def task_status_count(self, obj: 'Task'):
        return obj.status_logs.count()
    task_status_count.short_description = 'Task Status Count'


@admin.register(TaskPriority)
class TaskPriorityAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'label',
    )
