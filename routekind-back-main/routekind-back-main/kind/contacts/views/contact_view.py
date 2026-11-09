
from typing import TYPE_CHECKING

from django.db.models import Count
from django.http import HttpRequest

from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import APIException, ValidationError

from kind.addresses.models import Address
from kind.addresses.serializers import AddressSerializer
from kind.contacts.serializers import ContactSerializer, ContactAddressSerializer
from kind.generics.views.base_view import BaseModelViewSet

if TYPE_CHECKING:
    from kind.customauth.models import User


class ListAddressesMixin:
    addresses_related_name = None
    addresses_serializer_class = AddressSerializer

    def _serialize_addresses_qs(self, addresses_qs, request: HttpRequest, *, many=True):
        serializer = self.addresses_serializer_class(
            instance=addresses_qs, many=many, context={'request': request}
        )
        return serializer.data

    def _list_addresses_queryset(self, request: HttpRequest):
        # TODO: REDO
        # full_addresses_qs = Address.objects \
        #     .annotate(count=Count(self.addresses_related_name)) \
        #     .filter(count__gt=0)

        user: 'User' = request.user
        full_addresses_qs = Address.objects.filter(company=user.company)  # .filter(count__gt=0)

        if user.is_superuser:
            return full_addresses_qs
        else:
            return user.get_assigned_addresses(full_addresses_qs)

    def _list_addresses_response(self, request: HttpRequest):

        addresses_qs = self._list_addresses_queryset(request)

        # TODO: Apply filters
        # queryset = self.filter_queryset(self.get_queryset())

        list_all = request.GET.get('all') is not None

        if not list_all:
            page = self.paginate_queryset(addresses_qs)
            if page is not None:
                data = self._serialize_addresses_qs(page, request)
                return self.get_paginated_response(data)

        # if addresses_qs and addresses_qs.count() > 0:
        # addrs = addresses_qs.all()
        data = self._serialize_addresses_qs(addresses_qs, request)
        return Response(data)

    @action(detail=False, methods=['get'])
    def addresses(self, request: HttpRequest):

        if not self.addresses_related_name:
            raise APIException("addresses_related_name not defined in addresses action.")

        address_id = request.GET.get('id', None)

        if address_id is not None:
            instance = self._list_addresses_queryset(request).filter(id=address_id).first()
            data = self._serialize_addresses_qs(instance, request, many=False)
            return Response(data)

        return self._list_addresses_response(request)

    # @action(detail=True, methods=['get'])
    # def address(self, request: HttpRequest, pk=None):

    #     if not self.addresses_related_name:
    #         raise APIException("addresses_related_name not defined in addresses action.")

    #     instance = self._list_addresses_queryset(request).filter(id=pk).first()
    #     serializer = self.addresses_serializer_class(instance=instance)
    #     return Response(serializer.data)


class ContactView(BaseModelViewSet, ListAddressesMixin):
    serializer_class = ContactSerializer
    addresses_related_name = 'contacts'
    addresses_serializer_class = ContactAddressSerializer
