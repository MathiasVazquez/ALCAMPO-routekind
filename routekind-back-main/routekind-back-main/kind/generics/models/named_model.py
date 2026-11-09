import re
from django.db import models
from rest_framework.exceptions import ValidationError

from kind.generics.models import GenericBaseModel

from ..utils import validate_strict_name as is_valid_strict_name


class InvalidNameException(ValidationError):
    def __init__(self, detail=None, code=None):
        detail = 'El nombre debe iniciar con una letra y no puede contener espacios en blanco ni caracteres.'
        super().__init__(detail, code)


def validate_strict_name(value):
    if not is_valid_strict_name(value, raise_exception=False):
        raise InvalidNameException()


class StrictNamedModelMixin(models.Model):
    name = models.CharField(
        max_length=120,
        validators=[validate_strict_name]
    )

    def clean(self):
        # Llamamos al clean() de la clase padre
        super().clean()

        # Verificamos que sea único
        # TODO: MAKE IT!

        # if issubclass(self.__class__, GenericBaseModel):
        #     # Verificamos si existe otro objeto con la misma combinación de name y company
        #     has_module = hasattr(self, 'module')
        #     queryset = self.__class__.objects. \
        #         filter(name=self.name, company=self.company, **({"module": self.module} if has_module else {})). \
        #         exclude(id=self.id)
        #     if queryset.exists():
        #         if has_module:
        #             raise ValidationError(f"El nombre {self.name} ya existe y no puede repetirse en un mismo módulo.")
        #         else:
        #             raise ValidationError("El nombre {self.name} no puede repetirse.")

    def save(self, *args, **kwargs):
        # Run validations
        self.full_clean()
        # Return saved instance
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True
