from typing import List, TYPE_CHECKING

from rest_framework import serializers
from django.db.models import Case, When
from django.db.models.fields import Field
from django.db.models.query import QuerySet
from rest_framework.relations import PKOnlyObject

if TYPE_CHECKING:
    from kind.generics.views import BaseModelViewSet


class CurrentModuleDefault:
    requires_context = True
    requires_view = True

    def __call__(self, serializer_field):
        view: BaseModelViewSet = serializer_field.context['view']
        return view.get_module()

    def __repr__(self):
        return '%s()' % self.__class__.__name__


class CurrentCompanyDefault:
    requires_context = True

    def __call__(self, serializer_field):
        company = serializer_field.context['request'].user.company
        return company

    def __repr__(self):
        return '%s()' % self.__class__.__name__


class CurrentUserDefault:
    requires_context = True

    def __call__(self, serializer_field):
        user = serializer_field.context['request'].user
        return user

    def __repr__(self):
        return '%s()' % self.__class__.__name__


class OrderedFieldsSerializerMixin(serializers.ModelSerializer):
    KEEP_FIELDS_ORDERED = {}

    def __field_to_representation(self, field_name: str, value):
        """
        Field instance -> Primitive datatypes.
        """

        for field in self._readable_fields:
            field: Field = field
            if field.field_name != field_name:
                continue

            check_for_none = value.pk if isinstance(value, PKOnlyObject) else value
            if check_for_none is None:
                return None
            else:
                return field.to_representation(value)

        return None

    def to_representation(self, instance):
        ordered_fields = {}
        for field_name, through_name in self.KEEP_FIELDS_ORDERED.items():
            ordering: List[str] = getattr(instance, through_name)
            field_values: QuerySet = getattr(instance, field_name)
            if field_values.count() == 0 or len(ordering) == 0:
                continue

            ordered_field_values = field_values.order_by(
                Case(
                    *[
                        When(id=id_val, then=pos) for pos, id_val in enumerate(ordering)
                    ]
                )
            )
            ordered_fields[field_name] = self.__field_to_representation(field_name, ordered_field_values)

        data = super().to_representation(instance)
        data.update(**ordered_fields),
        return data

    def save(self, **kwargs):
        # Keet fields ordered
        for field_name, through in self.KEEP_FIELDS_ORDERED.items():
            elements: QuerySet = self.validated_data.get(field_name, None)
            if elements is not None:
                kwargs[through] = [str(elem.id) for elem in elements]

        # Return template instance
        return super().save(**kwargs)


class BaseModelSerializerMixin(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False, read_only=True)
    # module = serializers.HiddenField(default=CurrentModuleDefault())
    company = serializers.HiddenField(default=CurrentCompanyDefault())
    created_by = serializers.HiddenField(default=CurrentUserDefault(), label="Creado por")
    updated_by = serializers.HiddenField(default=CurrentUserDefault(), label="Modificado por")

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation.pop('polymorphic_ctype', None)
    #     return representation

    # def update(self, instance, validated_data: dict):
    #     request = self.context['request']
    #     validated_data['updated_by'] = request.user
    #     validated_data.pop('module', None)
    #     validated_data.pop('company', None)
    #     validated_data.pop('created_by', None)
    #     validated_data.pop('template', None)
    #     return super().update(instance, validated_data)
