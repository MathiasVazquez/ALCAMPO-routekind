from datetime import datetime
from typing import TYPE_CHECKING, List

from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework.response import Response

from kind.tasks.models import Task, TaskStatus
from kind.contacts.models import Contact
from kind.customauth.models import User

if TYPE_CHECKING:
    from kind.addresses.models import Address


class TasksReport1(APIView):

    def get(self, request: HttpRequest):
        try:
            data = TaskStatus.objects.all()  # values("created_at", "created_by", "task_id", "coords__address", "coords__latlng")
            response = [
                "Nombre de usuario;"
                "Nombre;",
                "Apellido;",
                "Nro documento;",
                "Teléfono;",
                "Nombre del comercio;",
                "ID cliente;",
                "Fecha;"
                "Hora;"
                "Rubros;"
                "Dirección;"
                "Coordenadas;"
                "Estado;"
                "Descripción$"
            ]
            for status in data:
                task: 'Task' = status.task
                contact_address: 'Address' = task.contact_address
                contact: 'Contact' = Contact.objects.get(addresses__id=contact_address.id)
                assigned_user: 'User' = task.users.first()

                if not assigned_user or assigned_user.is_connection_request(request):
                    continue

                rubros: List[str] = (contact.additional_values or {}).get("rubros", ["-"])
                rubros = ", ".join(rubros)

                status_data = status.data
                if not status_data:
                    status_data = ""
                elif status.name == "notaccepted":
                    reason = status_data.get("reason")
                    if reason == "Otros":
                        status_data = f"{reason}: {status_data.get('other_reason', '-')}"
                    else:
                        status_data = reason
                elif status.name == "revisit":
                    status_data = status_data.get("date")
                elif status.name == "accepted":
                    # [('sign', True), ('setting_up', True), ('capacitation', True), ('cobros_register', True)]
                    items = list(status_data.items())
                    status_data = ", ".join(key for key, value in items if value == True)
                    status_data = status_data \
                        .replace("cant_move", "No puede avanzar") \
                        .replace("full_register", "Apertura de cuenta full") \
                        .replace("cobros_register", "Registro en Pik cobros") \
                        .replace("capacitation", "Capacitación") \
                        .replace("test_transaction", "Transacción de prueba") \
                        .replace("sign", "Firma del formulario de entrega de máquina") \
                        .replace("setting_up", "Colocación de materiales") \
                        .replace("want_outgoing", "Quiere saliente")

                response.append(
                    f"{assigned_user.username}; "
                    f"{contact.first_name}; "
                    f"{contact.last_name}; "
                    f"{contact.document}; "
                    f"{contact.additional_values.get('phone', '-') if contact.additional_values else '-'}; "
                    f"{contact_address.description}; "
                    f"{contact.id}; "
                    f"{status.created_at.date()}; "
                    f"{status.created_at.time()}; "
                    f"{rubros}; "
                    f"{contact_address.coords.get('address') if contact_address.coords else '-'}; "
                    f"{contact_address.coords.get('latlng') if contact_address.coords else '-'}; "
                    # f"{status.name}; "
                    f"{status.label}; "
                    f"{status_data or '-'}$"
                )
            return Response("".join(response))
        except Exception as e:
            return Response(e.args)
