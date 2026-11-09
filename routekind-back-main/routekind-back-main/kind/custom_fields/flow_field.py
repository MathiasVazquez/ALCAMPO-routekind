from typing import Any, List
from datetime import datetime

from django.db import models
from django.db.models import Model
from rest_framework.exceptions import ValidationError
from rest_framework import serializers


"""
flow:
first_task_is_created=True (automatic)
[
    {
        name: "created",
        label: "Creado",
        color: "grey",
        transitions: [
            {
                name: "in_process",
                label: "Iniciar"
            },
            {
                name: "cancel",
                label: "Cancelar"
            },
        ]
    },
    {
        name: "in_process",
        label: "En camino",
        color: "blue",
        transitions: [
            {
                name: "finished",
                label: "Entregar",
                throught: "form" | "invoice" | "order" | "button" (default)
            },
            {
                name: "cancel",
                label: "Cancelar"
            },
        ]
    },
    {
        name: "cancel",
        label: "Cancelado",
        color: "red"
    },
    {
        name: "finished",
        label: "Entregado",
        color: "green"
    },
]

"""


class StrictSerializer(serializers.Serializer):
    """
    Un serializador que lanza una excepción ValidationError si hay campos desconocidos.
    """

    def to_internal_value(self, data):
        known_keys = set(self.fields)
        unknown_keys = set(data) - known_keys

        if unknown_keys:
            raise serializers.ValidationError(f"Unknown fields: {', '.join(unknown_keys)}")

        return super().to_internal_value(data)


class StatusTransitionFormFieldPropsSerializer(StrictSerializer):
    label = serializers.CharField(max_length=60)
    type = serializers.CharField(max_length=60, required=False)
    autofocus = serializers.BooleanField(default=False, required=False)
    required = serializers.BooleanField(default=False, required=False)


class StatusTransitionFormFieldSerializer(StrictSerializer):
    name = serializers.CharField(max_length=60)
    when = serializers.CharField(max_length=2040, required=False)
    choices = serializers.JSONField(default=list, required=False)
    props = StatusTransitionFormFieldPropsSerializer()
    fieldType = serializers.CharField(max_length=60, required=False)


class StatusTransitionFormSerializer(StrictSerializer):
    name = serializers.CharField(max_length=60)
    title = serializers.CharField(max_length=60)
    subtitle = serializers.CharField(max_length=510)
    validations = serializers.JSONField(default=list)
    fields = StatusTransitionFormFieldSerializer(many=True)

    def validate_validations(self, value: List[str]):
        if type(value) != list:
            raise ValidationError("This field must be a list.")

        if not all(type(elem) == str for elem in value):
            raise ValidationError("Each element of the list must be a string.")


class StatusTransitionSerializer(StrictSerializer):
    THROUGHT_CHOICES = (
        ("invoice", "Invoice"),
        ("order", "Order"),
        ("button", "Button"),
        ("form", "Form"),
        ("confirm", "Confirm"),
        ("invoice_cancel", "Invoice cancel"),
    )

    name = serializers.CharField(max_length=60)
    label = serializers.CharField(max_length=60)
    throught = serializers.ChoiceField(choices=THROUGHT_CHOICES, required=False)
    message = serializers.CharField(max_length=500, required=False)
    assigned_only = serializers.BooleanField(default=False, required=False)
    form = StatusTransitionFormSerializer(required=False)

    def validate_throught(self, value):
        form_data = self.data.get('form', None)
        if value == 'form' and not form_data:
            raise ValidationError({"form": "This field is required"})


class StatusFlowSerializer(StrictSerializer):
    TYPE_CHOICES = [
        ('p', 'In progress'),
        ('c', 'Completed'),
    ]

    name = serializers.CharField(max_length=60)
    label = serializers.CharField(max_length=60)
    color = serializers.CharField(max_length=60)
    transitions = StatusTransitionSerializer(many=True, required=False)
    type = serializers.ChoiceField(choices=TYPE_CHOICES)


class StatusFlowJSONField(models.JSONField):
    def clean(self, value: List[dict], model_instance):

        if not isinstance(value, list):
            raise ValidationError({"error": "The value must be a list."})

        status_serializer = StatusFlowSerializer(data=value, many=True)
        status_serializer.is_valid(raise_exception=True)

        # Validate transition names
        status_names = [status.get("name") for status in value]
        for status in value:
            transitions: List[dict] = status.get("transitions", None)
            if transitions is None:
                continue

            for index, transition in enumerate(transitions, start=1):
                transition_name = transition.get("name")
                transition_throught = transition.get("throught", None)

                if transition_throught is None:
                    continue
                if transition_name not in status_names:
                    raise ValidationError({
                        "error": f"The name '{transition_name}' for transition at position {index} of status {status.get('name')} is not valid."
                    })

        return super().clean(value, model_instance)

    def pre_save(self, model_instance: Model, add: bool) -> Any:
        flow = super().pre_save(model_instance, add)

        return flow

    def get_old_info(self, model_instance):
        current_instance = type(model_instance).objects.filter(pk=model_instance.pk).first()
        return getattr(current_instance, self.attname) if current_instance else None
