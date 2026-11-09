import re
from typing import TYPE_CHECKING

from django.db import models

from kind.generics.models.base_model import CustomModelAbstract
from kind.custom_fields import CoordsJSONField
from kind.generics.utils import eval_contextualized_js_code
from kind.tasks.models import Task
from kind.tasks.models.task_model import StatusFlowTemplate
from encrypted_model_fields.fields import EncryptedCharField

if TYPE_CHECKING:
    from kind.contacts.models import Contact


class Address(CustomModelAbstract):
    auto_id = models.BigIntegerField(default=0)
    description = EncryptedCharField(max_length=2040, default="", blank=True)
    coords: dict = CoordsJSONField(default=None, null=True)
    created_coords: dict = CoordsJSONField(default=None, null=True)
    tasks: 'models.Manager'
    # contacts: 'models.Manager'
    additional_fields = models.JSONField(default=None, null=True, blank=True)
    contact: 'Contact' = models.ForeignKey(
        'contacts.Contact',
        on_delete=models.SET_NULL,
        default=None,
        blank=True,
        null=True,
        related_name='addresses'
    )

    # Create initial task
    def _format_task_text(self, text: str, default_value=""):
        if not text:
            return default_value

        data = {
            "contact": {
                "id": self.contact.id,
                "full_name": self.contact.full_name,
                "first_name": self.contact.first_name,
                "last_name": self.contact.last_name,
                "document": self.contact.document,
                **(self.contact.additional_values or {}),
            } if self.contact is not None else {},
            "id": self.id,
            "description": self.description,
            "coords": self.coords,
            **(self.additional_fields or {}),
        }

        try:
            def replace(match):
                path = match.group(1).split('.')
                try:
                    value = data
                    for key in path:
                        value = value[key]
                    # Si el valor es None, devolver un string vacío
                    if value is None:
                        return ''
                    return str(value)
                except KeyError:
                    return ''  # Si la clave no existe, retorna un string vacío

            result = re.sub(r'\{([^\}]+)\}', replace, text)
            return re.sub(r'\s{2,}', ' ', result).strip()
        except:
            pass

        return default_value

    def get_initial_flow(self):
        company = self.company
        _default = company.default_on_create_address_task_template

        if not company.address_custom_fields_meta:
            return _default

        select_flow_code = company.address_custom_fields_meta.get('selectFlow')
        if not select_flow_code:
            return _default

        # Eval custom form select flow code
        data = {
            **(self.additional_fields or {}),
            "addressDescription": self.description,
            "coords": self.coords,
            "contact": {
                **(self.contact.additional_values or {}),
                "firstName": self.contact.first_name,
                "lastName": self.contact.last_name,
                "document": self.contact.document
            } if self.contact else None
        }
        result_flow_name = eval_contextualized_js_code(select_flow_code, data)
        if not result_flow_name:
            return _default

        select_flow = StatusFlowTemplate.objects.filter(company=company, name=result_flow_name).first()

        return select_flow if select_flow is not None else _default

    def create_first_task(self):
        self.refresh_from_db()

        initial_flow = self.get_initial_flow()

        if initial_flow is None:
            return

        # Use custom form flow

        # Create first address' task
        task = Task.objects.create(
            subject=self._format_task_text(
                initial_flow.default_tasks_subject,
                f"{self.description}"
            ),
            description=self._format_task_text(
                initial_flow.default_tasks_description,
            ),
            flow=initial_flow,
            contact_address=self,
            company=self.company,
            created_by=self.created_by,
            updated_by=self.created_by,
        )
        task.users.add(self.created_by)
        task.save()

        # Set first status coords
        if self.created_coords:
            status = task.current_status.__class__.objects.get(id=task.current_status.id)
            status.coords = {"latlng": self.created_coords.get('latlng')}
            status.save()

        return task

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.auto_id = self.company.addresses_auto_enumeration + 1
            self.company.addresses_auto_enumeration = self.auto_id
            self.company.save()

        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.description} - {self.contact}"
