
from typing import TYPE_CHECKING, cast, List

from django.http import HttpRequest
from rest_framework import serializers

from kind.contacts.serializers.contact_address_serializer import ContactAddressSerializer
from kind.customauth.serializers.user_serializer import UserSerializer
from kind.useraudit.models import UserAudit
from kind.orders.serializers.orders_serializer import OrderSerializer
from kind.sales.serializers.invoice_serializer import InvoiceSerializer
from kind.tasks.models import Task, TaskStatus, StatusFlowTemplate
from kind.generics.serializers import BaseSerializer
from kind.tasks.serializers.task_priority_serializer import TaskPrioritySerializer
from kind.customauth.models import User

if TYPE_CHECKING:
    from kind.companies.models import Company


class StatusFlowTemplateSerializer(BaseSerializer):

    class Meta:
        model = StatusFlowTemplate
        fields = '__all__'


class TaskStatusSerializer(BaseSerializer):
    label = serializers.ReadOnlyField()
    color = serializers.ReadOnlyField()
    type = serializers.ReadOnlyField()
    transitions = serializers.ReadOnlyField()
    data = serializers.ReadOnlyField()

    class Meta:
        model = TaskStatus
        fields = '__all__'


class TaskStatusLogsUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = [
            'id',
            'name',
            'username',
            'email',
        ]


class TaskStatusLogsSerializer(BaseSerializer):
    label = serializers.ReadOnlyField()
    color = serializers.ReadOnlyField()
    type = serializers.ReadOnlyField()
    created_by = serializers.SerializerMethodField()  # TaskStatusLogsUserSerializer()
    data_form = serializers.SerializerMethodField()

    def get_created_by(self, instance: 'TaskStatus'):
        user = instance.created_by or cast(Task, instance.task).users.first()
        return TaskStatusLogsUserSerializer(user, context=self.context).data
        # return user.name or user.username if user else None

    def get_data_form(self, instance: 'TaskStatus'):
        prev_step = None
        for step in instance.task.flow.steps:
            if step.get('name') == instance.previous_status_name:
                prev_step = step
                break

        if not prev_step:
            return None

        transition: dict = [
            t for t in prev_step.get('transitions')
            if t.get('name') == instance.name
        ][0]

        form: dict = transition.get('form')

        if not form:
            return None

        form_fields: List[dict] = form.get('fields')

        form = {}
        for field in form_fields:
            name = field.get('name')
            props: dict = field.get('props')
            value = props.get('label') if props else name
            form[name] = {
                "label": value,
                "fieldType": field.get('fieldType') or 'input'
            }

        return form

    class Meta:
        model = TaskStatus
        fields = (
            "id",
            "label",
            "color",
            "type",
            "coords",
            "created_at",
            "created_by",
            "data",
            "data_form",
        )


class TaskSerializer(BaseSerializer):

    current_status = serializers.SerializerMethodField()
    status_logs = TaskStatusLogsSerializer(many=True, required=False)
    invoice = InvoiceSerializer(many=False, required=False)
    order = OrderSerializer(many=False, required=False)
    contact_address = ContactAddressSerializer(many=False, required=False)
    priority = TaskPrioritySerializer(many=False, required=False)
    is_expired = serializers.ReadOnlyField()
    is_completed = serializers.ReadOnlyField()

    def get_current_status(self, instance: 'Task'):
        data = TaskStatusSerializer(instance.current_status, context=self.context).data

        request: HttpRequest = self.context.get('request', None)
        user: "User" = request.user
        company: "Company" = user.company

        is_assigned_user = instance.users.filter(id=request.user.id).exists()
        is_assigned_sales_point = (
            user.assigned_sales_point is not None and
            instance.sales_points.filter(id=user.assigned_sales_point.id).exists()
        ) and company.enable_sales_points

        if instance.is_completed is None:
            instance.is_completed = instance.current_status.type == "c"

        if not is_assigned_user and not is_assigned_sales_point:
            data['transitions'] = []

        return data

    def create(self, validated_data: dict):
        task: 'Task' = super().create(validated_data)

        # Create audit register
        UserAudit.add_tasks_log(
            task,
            self.get_user(),
            self.ip_address,
            self.device_name,
            created=True
        )

        return task

    def update(self, instance, validated_data):
        task: 'Task' = super().update(instance, validated_data)

        # Audit update
        request_data: dict = self.context.get('request').data
        current_status: dict = request_data.get('current_status', None)
        users: list = request_data.get('users', None)
        start_date: str = request_data.get('start_date', None)
        end_date: str = request_data.get('end_date', None)
        ip_address = self.ip_address
        device_name = self.device_name

        if current_status is not None:
            # Audit status changed
            UserAudit.add_task_status_change_log(
                task,
                self.get_user(),
                self.instance.current_status,
                ip_address,
                device_name,
            )
        if users is not None or start_date or end_date:
            entry_status = {
                **({"users": list(User.objects.filter(id__in=users).values_list('username', flat=True))} if users is not None else {}),
                **({"start_date": start_date} if start_date else {}),
                **({"end_date": end_date} if end_date else {}),
            }
            UserAudit.add_tasks_log(
                task,
                self.get_user(),
                ip_address,
                device_name,
                entry_status=entry_status
            )

        return task

    def save(self, **kwargs):
        request_data: dict = self.context.get('request').data
        current_status: dict = request_data.get('current_status', None)

        if current_status is not None:
            request_user: "User" = self.context.get('request').user
            coords = request_data.pop('coords', None)
            data = request_data.pop('data', None)
            self.instance: 'Task'
            self.instance.current_status = TaskStatus(
                name=current_status.get('name', None),
                coords=coords,
                data=data,
                created_by=request_user,
                updated_by=request_user,
                previous_status_name=self.instance.current_status.name,
            )

        return super().save(**kwargs)

    # def create(self, validated_data):
    #     result: 'Task' = super().create(validated_data)
    #     result.users.add(self.add)
    #     return result

    class Meta:
        model = Task
        fields = '__all__'
        ordering = ["-created_at"]
