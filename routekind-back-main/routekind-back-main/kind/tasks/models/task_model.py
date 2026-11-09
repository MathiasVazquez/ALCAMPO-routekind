
from typing import TYPE_CHECKING, List

from django.utils import timezone
from django.db import models
from rest_framework.exceptions import ValidationError

from kind.custom_fields.coords_field import CoordsJSONField
from kind.custom_fields.crypted_json_field import CryptedJSONField
from kind.custom_fields.flow_field import StatusFlowJSONField
from kind.customauth.models.mixins import AssignableMixin
from kind.generics.models.base_model import CustomModelAbstract
from kind.generics.models.named_model import StrictNamedModelMixin
from kind.generics.utils import validate_strict_name
from encrypted_model_fields.fields import EncryptedCharField

if TYPE_CHECKING:
    from kind.sales.models import Invoice
    from kind.orders.models import Order
    from kind.companies.models import Company


class StatusFlowTemplate(CustomModelAbstract, StrictNamedModelMixin):
    label = models.CharField(max_length=120)
    description = models.CharField(max_length=2040)
    steps: List[dict] = StatusFlowJSONField()
    admin_required = models.BooleanField(default=False)

    default_tasks_subject = models.CharField(max_length=1020, default=None, null=True, blank=True)
    default_tasks_description = models.CharField(max_length=2040, default=None, null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    @classmethod
    def create_default_orders_template(cls, company: 'Company'):
        steps = [
            {
                "name": "pending",
                "label": "Pendiente",
                "color": "grey",
                "type": "p",
                "transitions": [
                    {
                        "name": "finished",
                        "label": "Entregar con factura",
                        "throught": "invoice",
                    },
                    {
                        "name": "finished",
                        "label": "Marcar como entregado",
                        "throught": "confirm",
                        "confirm_message": "¿Está seguro de que desea marcar este pedido como entregado?",
                    },
                    {
                        "name": "cancel",
                        "label": "Cancelar entrega",
                        "throught": "confirm",
                        "confirm_message": "¿Está seguro de que desea cancelar este pedido?",
                    },
                ]
            },
            # {
            #     "name": "in_process",
            #     "label": "En camino",
            #     "color": "blue",
            #     "transitions": [
            #         {
            #             "name": "finished",
            #             "label": "Entregar",
            #             "throught": "form" | "invoice" | "order" | "button"
            #         },
            #         {
            #             "name": "cancel",
            #             "label": "Cancelar"
            #         },
            #     ]
            # },
            {
                "name": "cancel",
                "label": "Cancelado",
                "color": "red",
                "type": "c",
            },
            {
                "name": "finished",
                "label": "Entregado",
                "color": "green",
                "type": "c",
            }
        ]
        company.default_orders_task_template = StatusFlowTemplate(
            name='default_orders_tasks_flow_template',
            label="Default orders flow",
            description="",
            steps=steps,
            company=company,
        )
        company.default_orders_task_template.save()
        company.save()

    @classmethod
    def create_default_invoices_template(cls, company: 'Company'):
        steps = [
            {
                "name": "created",
                "label": "Creado",
                "color": "green",
                "type": "c",
                "transitions": [
                    {
                        "name": "cancel",
                        "label": "Anular",
                        "throught": "invoice_cancel"
                    },
                ]
            },
            {
                "name": "cancel",
                "label": "Cancelado",
                "color": "red",
                "type": "c",
            },
        ]
        company.default_invoices_task_template = StatusFlowTemplate(
            name='default_invoices_tasks_flow_template',
            label='Default invoices flow',
            description='',
            steps=steps,
            company=company,
        )
        company.default_invoices_task_template.save()
        company.save()

    @classmethod
    def create_default_task_template(cls, company: 'Company'):
        steps = [
            {
                "name": "created",
                "label": "Creado",
                "color": "grey",
                "type": "p",
                "transitions": [
                    {
                        "name": "finished",
                        "label": "Finalizar"
                    },
                    {
                        "name": "cancel",
                        "label": "Cancelar"
                    },
                ]
            },
            {
                "name": "finished",
                "label": "Completado",
                "color": "green",
                "type": "c",
            },
            {
                "name": "cancel",
                "label": "Cancelado",
                "color": "red",
                "type": "c",
            },
        ]
        company.default_tasks_template = StatusFlowTemplate(
            name='default_tasks_flow_template',
            label='Default tasks flow',
            description='',
            steps=steps,
            company=company,
        )
        company.default_tasks_template.save()
        company.save()


class TaskStatus(CustomModelAbstract):
    name = models.CharField(
        max_length=120,
        validators=[validate_strict_name]
    )
    # label = models.CharField(max_length=510)
    datetime = models.DateTimeField(default=timezone.now)
    # is_final = models.BooleanField(default=False)
    coords: dict = CoordsJSONField(default=None, null=True, blank=True)
    task: 'Task' = models.ForeignKey(
        'Task',
        related_name="status_logs",
        on_delete=models.CASCADE,
    )
    previous_status_name = models.CharField(max_length=60, null=True, blank=True)
    data: dict = CryptedJSONField(default=None, null=True, blank=True)

    @property
    def _flow_status(self) -> dict:
        results = [
            step
            for step in self.task.flow.steps
            if step.get("name") == self.name
        ]
        return results[0]

    @property
    def transitions(self) -> List[dict]:
        return self._flow_status.get("transitions", [])

    @property
    def color(self) -> str:
        return self._flow_status.get("color")

    @property
    def type(self) -> str:
        return self._flow_status.get("type")

    @property
    def label(self) -> str:
        return self._flow_status.get("label")

    def __str__(self) -> str:
        return f"'{self.name}' status for task '{self.task}'"


class Task(CustomModelAbstract, AssignableMixin):
    auto_id = models.BigIntegerField(default=0)
    subject = EncryptedCharField(max_length=510)
    description = EncryptedCharField(max_length=2040, default="", blank=True)
    is_completed = models.BooleanField(default=None, null=True)
    flow = models.ForeignKey(
        StatusFlowTemplate,
        blank=True,
        on_delete=models.PROTECT,
    )
    contact_address = models.ForeignKey(
        'addresses.Address',
        related_name='tasks',
        on_delete=models.PROTECT,
    )
    status_logs: models.Manager
    invoice: 'Invoice' = models.ForeignKey(
        'sales.Invoice',
        null=True,
        blank=True,
        related_name='tasks',
        on_delete=models.SET_NULL,
    )
    order: 'Order' = models.ForeignKey(
        'orders.Order',
        null=True,
        blank=True,
        related_name='tasks',
        on_delete=models.SET_NULL,
    )
    # sales_points = models.ManyToManyField(
    #     'inventory.SalesPoint',
    #     blank=True,
    #     related_name='tasks',
    # )
    # users = models.ManyToManyField(
    #     'customauth.User',
    #     blank=True,
    #     related_name='tasks',
    # )
    priority = models.ForeignKey(
        'tasks.TaskPriority',
        blank=True,
        null=True,
        related_name='tasks',
        on_delete=models.SET_NULL,
    )
    start_date = models.DateTimeField(default=None, null=True, blank=True)
    due_date = models.DateTimeField(default=None, null=True, blank=True)

    @property
    def current_status(self) -> 'TaskStatus':
        return self.status_logs.order_by('datetime').last()

    @property
    def is_expired(self):
        if not self.due_date:
            return False
        if self.current_status.type == 'c':
            return False
        now_aware = timezone.now()
        return now_aware > self.due_date

    @current_status.setter
    def current_status(self, value: 'TaskStatus'):
        self._is_valid_next_status(value.name, raise_exception=True)
        value.task = self
        value.company = self.company
        value.save()

    def _on_create(self):
        company: 'Company' = self.company

        # SET AUTO ID
        self.auto_id = self.company.tasks_auto_enumeration + 1
        self.company.tasks_auto_enumeration = self.auto_id
        self.company.save()

        # Create default flow
        # TODO: FIX?
        # if not self.flow and not company.default_tasks_template:
        #     print("######## Create a default template?")
        #     StatusFlowTemplate.create_default_task_template(company)

        # Set default flow
        if not hasattr(self, 'flow') or not self.flow:
            self.flow = company.default_tasks_template

        # Set default priority
        if not hasattr(self, 'priority') or not self.priority:
            self.priority = company.default_task_priority

        # Set initial state
        self.current_status = TaskStatus(
            name=self.flow.steps[0].get('name'),
            created_by=self.created_by,
            updated_by=self.updated_by,
        )

    def _is_valid_next_status(self, next_status_name: str, *, raise_exception=False):
        current_status = self.current_status
        if (
            not current_status or
            current_status.name == next_status_name
        ):
            return True

        prev_status_transitions: List[dict] = [
            step for step in self.flow.steps if step.get('name') == current_status.name
        ][0].get('transitions', None)

        if not prev_status_transitions or len(prev_status_transitions) == 0:
            if raise_exception:
                raise ValidationError({'error': f"'{next_status_name}' is not a valid transition."})
            return False

        valid_next_status = [transition.get("name") for transition in prev_status_transitions]
        if next_status_name not in valid_next_status:
            if raise_exception:
                raise ValidationError({'error': f"'{next_status_name}' is not a valid transition."})
            return False
        return True

    def save(self, *args, **kwargs):
        # Handle creating events
        if self._state.adding:
            self._on_create()

        # Set is completed by current_status
        self.is_completed = self.current_status.type == "c"

        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.subject} in {self.contact_address}"

    class Meta:
        ordering = ['-created_at']
