import uuid
from typing import Any, TYPE_CHECKING

from django.db import models
from django.http import HttpRequest
from rest_framework.exceptions import ValidationError, APIException

from kind.generics.serializers.base_seriaizer import _get_connection_module

if TYPE_CHECKING:
    from kind.customauth.models import User
    from kind.companies.models import Company


class CompanyBasedModelManager(models.Manager):
    def get_queryset_by_company(self, request):
        company = request.user.company
        return super().get_queryset().filter(company=company)

    def _validate_company_is_in_query(self, **kwargs):
        company = kwargs.get('company', None)
        company_id = kwargs.get('company_id', None)
        company__id = kwargs.get('company__id', None)
        if company is None and company_id is None and company__id is None:
            raise APIException('Company is not defined in objects filter.')

    def filter(self, *args, **kwargs):
        self._validate_company_is_in_query(**kwargs)
        return super().filter(*args, **kwargs)

    def get(self, *args: Any, **kwargs: Any):
        self._validate_company_is_in_query(**kwargs)
        return super().get(*args, **kwargs)

    def all(self, *, company=None):
        if company is not None:
            return self.filter(company=company)
        return super().all()


# pylint: disable=maybe-no-member
class GenericBaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y hora de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha y hora de modificación")
    is_active = models.BooleanField(default=True, verbose_name="Está activo")
    # client_id = models.TextField(default="", null=True, blank=True)
    company: 'Company' = models.ForeignKey(
        'companies.Company',
        null=True,
        related_name='%(app_label)s_%(class)s_instances',
        on_delete=models.PROTECT,
    )
    created_by: 'User' = models.ForeignKey(
        'customauth.User',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='%(app_label)s_%(class)s_create_user',
    )
    updated_by: 'User' = models.ForeignKey(
        'customauth.User',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='%(app_label)s_%(class)s_update_user',
    )

    @classmethod
    def get_connection_module(self, module, request: HttpRequest):
        return _get_connection_module(module, request)

    @classmethod
    def get_local_id_by_client_id(self, client_id: str, module, request: HttpRequest):
        connection_module = GenericBaseModel.get_connection_module(module, request)
        return connection_module.get_local_id_from_client_id(client_id)

    # objects = CompanyBasedModelManager()

    # def validate_unique(self, exclude=None):
    #     # VALIDATE UNIQUE CLIENT_ID PER COMPANY
    #     duplicates = self.__class__.objects.filter(
    #         client_id__isnull=False,
    #         client_id=self.client_id,
    #         company_id=self.company_id
    #     ).exclude(client_id__exact='').exclude(id=self.id)
    #     if duplicates.exists():
    #         raise ValidationError(
    #             f"client_id must be unique per company, but client_id '{self.client_id}' is duplicated")

    #     super(GenericBaseModel, self).validate_unique(exclude=exclude)

    def save(self, *args, **kwargs):
        # Validate client_id is unique per company
        # self.validate_unique()

        # Check that all entities have company assigned
        # Only company may not have another company assigned
        if self.company is None:
            from kind.companies.models import Company
            if type(self) is not Company:
                raise APIException(
                    f"Company not defined on instance of type '{self.__class__.__name__}'"
                )

        return super().save(*args, **kwargs)

    class Meta:
        abstract = True
