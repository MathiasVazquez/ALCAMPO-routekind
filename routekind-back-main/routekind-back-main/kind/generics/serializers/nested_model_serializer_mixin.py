from django.db import models
from rest_framework import serializers
from rest_framework.serializers import ListSerializer
from rest_framework.exceptions import ValidationError, APIException

from kind.generics.serializers.base_model_serializer_mixin import BaseModelSerializerMixin

from .utils import get_request_data_from_context


class NestedModelSerializerMixin(BaseModelSerializerMixin):
    unique_identifiers = ["id"]

    def to_internal_value(self, data):
        if not data:
            return None

        if isinstance(data, str):

            # Si el dato es un string, intenta buscar el producto por su ID
            try:
                return self.Meta.model.objects.get(id=data)
            except:
                raise ValidationError({"error": f"'{data}' not found"})
        # Si el dato es un diccionario, procede como normalmente
        return super().to_internal_value(data)

    def is_valid(self, raise_exception=False):
        # Extract related objects data before validate (it will be process later)
        request_data = get_request_data_from_context(self.context, raise_exception=True)
        [
            self.related_objects_data,
            self.related_primary_relations_data,
        ] = self.__get_related_objects_data(request_data)
        # Remove related objects data from validated data
        for related_objects_data_key in self.related_objects_data:
            self.context.get("request").data.pop(related_objects_data_key, None)
        # Check is valid
        return super().is_valid(raise_exception=raise_exception)

    def save(self, **kwargs):
        # Process direct relations
        self.process_primary_relation_objects(self.related_primary_relations_data)
        # Save instance
        instance = super().save(**kwargs)
        # Process related data
        self.process_related_objects(instance, self.related_objects_data)
        # Return instance
        return instance

    def process_primary_relation_objects(self, related_objects_data: dict):
        # Iterate over related objects
        for key, value in related_objects_data.items():
            # If the related object is not a list, but an dict...
            if isinstance(value, dict):
                processed_instance = self.create_or_update_related_objects(key, value)
                self._validated_data[key] = processed_instance

    def process_related_objects(self, instance, related_objects_data: dict):
        # Iterate over related objects
        for key, value in related_objects_data.items():
            # If the related object content is a list...
            if isinstance(value, list):
                # Related model and field
                related_model = self.Meta.model._meta.get_field(key).remote_field.related_model
                related_model_remote_field = getattr(related_model, key)
                # Extract the name of the field that represents the relation.
                # For example, if 'instance' is a model object of type 'Project',
                # and there is a 'project' field in User model that makes the relation
                # between 'Project' and 'User', then the value of 'parent_field_name'
                # will be the name of that property: 'project'
                parent_field_name = related_model_remote_field.rel.name
                if parent_field_name == key:
                    parent_field_name = related_model_remote_field.field.name
                # Check if the relation between the model of the key and the model of
                # this serializer is a many to many relation
                is_many_to_many = related_model_remote_field.rel.many_to_many
                # Iterate over the values of the list
                processed_instances_ids = []
                for data in value:
                    # If not a many to many relation:
                    # Set the 'parent_field_name' property key (with the value as its pk)
                    # to the data that will be serialized, so the relation can be defined
                    if not is_many_to_many:
                        data[parent_field_name] = instance.pk

                    # Create or update related object and get the instance
                    related_instance = self.create_or_update_related_objects(key, data)
                    processed_instances_ids.append(related_instance.id)

                    # Add element to many to many relation
                    if is_many_to_many:
                        getattr(instance, key).add(related_instance)

                # Delete non-present related registers
                if not is_many_to_many:
                    getattr(instance, key).all().exclude(
                        id__in=processed_instances_ids
                    ).delete()
                # Remove not more included instances
                else:
                    field_elements = getattr(instance, key)
                    for element in field_elements.all().exclude(id__in=processed_instances_ids):
                        field_elements.remove(element)

            # If the related object is not a list, but an dict...
            elif isinstance(value, dict):
                related_instance = self.create_or_update_related_objects(key, value)
                if hasattr(instance, key):
                    setattr(instance, key, related_instance)

            # If there is not a list or an object (never should happen...)
            else:
                raise APIException("Unexpected error")

        # Save changes in the instance and return
        instance.save()
        return instance

    def create_or_update_related_objects(self, name: str, data: dict):
        # Extract the related model of the list, for example,
        # if the related object is a list of users,
        # then 'related_model' will be the model User
        related_model = self.Meta.model._meta.get_field(name).remote_field.model
        # Extract serializer class to be used to create or update the model instance
        serializer_class = self.__get_serializer_class_by_name(name)
        # Create the context for the related objects serializers
        context = {**self.context, "data": data}

        # Get instance
        instance = self.get_instance_by_unique_identifiers(
            model_class=related_model,
            data=data,
            name=name,
        )

        # If there is an instance indentified, then, updated it
        if instance is not None:
            child_instance = instance
            # Update by serializer
            serializer: 'NestedModelSerializerMixin' = None
            if isinstance(data, dict):
                _data = {**data}
                _data.pop("client_id")
                serializer: 'NestedModelSerializerMixin' = serializer_class(
                    data=_data,
                    instance=child_instance,
                    context={**context, "data": _data},
                    partial=True,
                )
        # If there is not a valid identifier (or identificable object),
        # a new object will be created
        elif isinstance(data, dict):
            serializer: 'NestedModelSerializerMixin' = serializer_class(
                data=data,
                context=context,
                # partial=True
            )
        else:
            # The data must be a dict to be able to create a new instance.
            # If data is not a dict, raise an exception
            raise ValidationError()

        if serializer is not None:
            # Validate and save the serializer
            serializer.is_valid(raise_exception=True)
            # Return the crerated or updated instance
            return serializer.save()

        # No need to update or create any instance, so return the identified child instance
        return child_instance

    def __get_related_objects_data(self, data: dict):
        from .nested_model_serializer_mixin import NestedModelSerializerMixin
        related_primary_relations_data = {}
        related_objects_data = {}
        for field_name, field in self.fields.items():
            # Extract related list field name from data
            if isinstance(field, serializers.ListSerializer):
                if field.child and issubclass(field.child.__class__, NestedModelSerializerMixin):
                    if not field_name in data:
                        continue
                    related_objects_data[field_name] = data.pop(field_name, None)
            # Extract related dict field name from data
            elif (
                isinstance(field, NestedModelSerializerMixin)
                and field_name in data
                and type(data[field_name]) == dict
            ):
                # related_objects_data[field_name] = data.pop(field_name, None)
                related_primary_relations_data[field_name] = data.pop(field_name, None)

        return [related_objects_data, related_primary_relations_data]

    def __get_serializer_class_by_name(self, key: str):
        field = self.fields[key]
        return field.child.__class__ if isinstance(field, ListSerializer) else field.__class__

    def get_instance_by_unique_identifiers(self, *, name=None, data=None, instance=None, model_class=None):
        unique_identifiers = NestedModelSerializerMixin.__get_unique_identifiers(
            instance=instance,
            model_class=model_class,
            aditional_unique_identifiers=self.unique_identifiers
        )
        # Get the properties of data that can be used to identify uniquely to an instance
        reduced_unique_identifiers = self.reduce_unique_identifier(unique_identifiers, data)
        #  Use client id to get local id
        if (
            reduced_unique_identifiers is None and
            (client_id := data.get('client_id')) is not None
        ):
            reduced_unique_identifiers = {
                "id": model_class.get_local_id_by_client_id(
                    client_id,
                    model_class,
                    self.context.get('request')
                )
            }

        # Identify the instance, if exists
        if reduced_unique_identifiers is None:
            child_instance_filter = None
        else:
            child_instance_filter = model_class.objects.filter(
                **reduced_unique_identifiers
            )

        # Search for instance by identifiers
        if reduced_unique_identifiers is not None and child_instance_filter.exists():
            # Validater that there is only a single object in the filter
            if (child_instance_filter.count() > 1):
                raise APIException(
                    f'There is more than one result in objects of type '
                    f'{name}" with identifier: {reduced_unique_identifiers}'
                )
            return child_instance_filter.first()

        return None

    @classmethod
    def __get_unique_identifiers(cls, *, instance=None, model_class=None, aditional_unique_identifiers=None):

        if instance:
            if instance.unique_identifiers is not None:
                if cls.__check_unique_identifiers_is_valid(
                    instance.unique_identifiers,
                    raise_exception=True
                ):
                    return instance.unique_identifiers
            model = instance.Meta.model
        else:
            model = model_class

        local_unique_identifiers = []
        for field in model._meta.fields:
            if any([
                isinstance(field, models.AutoField),
                field.unique,
                field.unique_for_date,
                field.unique_for_month,
                field.unique_for_year
            ]):
                local_unique_identifiers.append(field.name)
            elif hasattr(field, "unique_together") and field.unique_together:
                local_unique_identifiers.append(field.unique_together)
        return list(set(local_unique_identifiers + (aditional_unique_identifiers or [])))

    @classmethod
    def __check_unique_identifiers_is_valid(cls, unique_identifiers, raise_exception=True):
        stack = [(unique_identifiers, 2)]
        while stack:
            current, lvl = stack.pop()
            if lvl < 0:
                if raise_exception:
                    raise ValidationError("Unique fields list should be of type [str] or [[str]]")
                return False
            if isinstance(current, str):
                continue
            elif isinstance(current, list):
                if lvl == 0:
                    if raise_exception:
                        raise ValidationError("Unique fields list should be of type [str] or [[str]]")
                    return False
                for element in current:
                    stack.append((element, lvl - 1))
            else:
                if raise_exception:
                    raise ValidationError("Unique fields list should be of type [str] or [[str]]")
                return False
        return True

    @classmethod
    def reduce_unique_identifier(cls, unique_identifiers: list, data: dict):
        if isinstance(data, str):
            return {"pk": data}

        for key in unique_identifiers:
            if isinstance(key, str) and key in data:
                return {key: data[key]}
            elif isinstance(key, list):
                uniques = []
                for sub_key in key:
                    if sub_key not in data:
                        break
                    uniques.append(data[sub_key])
                else:  # not-break
                    return dict(zip(key, uniques))
        return None
