from typing import Any, List

from django.db import models
from django.db.models import Model
from rest_framework.exceptions import ValidationError
from rest_framework import serializers


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


class ZonePeriodicityRulesSerializer(serializers.Serializer):
    # name = models.CharField(required=False)
    type = models.CharField()
    values = models.JSONField()


class ZonePeriodicitySerializer(serializers.Serializer):
    asociation = serializers.CharField()
    rules = ZonePeriodicityRulesSerializer(many=True)


class ZonePeriodicityRulesJSONField(models.JSONField):
    def clean(self, value: dict, model_instance):

        if value:
            if not isinstance(value, dict):
                raise ValidationError({"error": "The value must be an object."})

            periodicity_serializer = ZonePeriodicitySerializer(data=value)
            periodicity_serializer.is_valid(raise_exception=True)

            # Validate asociation
            asociation: str = value.get('asociation')
            rules: List[dict] = value.get('rules')
            # names = [rule.get("name") for rule in rules]

            if not asociation:
                asociation = value['asociation'] = 'and'

            if asociation not in ['and', 'or']:
                raise ValidationError({'error': "The defined asociation is not valid."})

            if not all(type(rule.get('values')) == list for rule in rules):
                raise ValidationError({'values': "This field must be a list."})

            # TODO: usar expresión regular
            # regex_pattern = r"(\b[a-zA-Z][a-zA-Z0-9]*\b|\(|\)|or|and|\s)+"
            # return bool(re.fullmatch(regex_pattern, text.strip()))

            # formatted_asociation = asociation \
            #     .replace("(", "") \
            #     .replace(")", "") \
            #     .replace("or", "") \
            #     .replace("and", "")

            # formatted_asociation_words = [a.strip() for a in formatted_asociation.split(" ") if len(a.strip()) > 0]
            # all_words_are_valid = all(word in names for word in formatted_asociation_words)

            # if not all_words_are_valid or all_words_are_valid in ['and', 'or']:
            #     raise ValidationError({'error': 'The defined asociation is not valid.'})

        return super().clean(value, model_instance)

    def pre_save(self, model_instance: Model, add: bool) -> Any:
        return super().pre_save(model_instance, add)

    def save_form_data(self, instance: Model, data: Any) -> None:
        if not data:
            data = {
                "asociation": 'and',
                "rules": [
                    {
                        "type": "ever",
                        "values": []
                    }
                ]
            }
        return super().save_form_data(instance, data)

    def evatuate(self):
        pass
