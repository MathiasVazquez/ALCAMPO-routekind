from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
import math


class OptionalPagination(PageNumberPagination):
    def get_page_size(self, request):
        return 24

    def paginate_queryset(self, queryset, request, view=None):
        self.request = request
        self.queryset = queryset  # Guarda el queryset para usarlo más tarde

        # Si 'all' está presente en los parámetros, retorna None para desactivar la paginación
        if 'all' in request.query_params:
            return None

        # Si 'page' está presente en los parámetros, aplica la paginación estándar
        if 'page' in request.query_params:
            return super().paginate_queryset(queryset, request, view)

        # Si no hay parámetros relevantes, evita paginar pero prepara para metadatos
        return []

    def get_paginated_response(self, data):
        # Si se solicita sin paginación ('all'), devuelve todos los datos
        if 'all' in self.request.query_params:
            data = list(self.queryset)
            return Response(data)

        # Si no se ha solicitado una página específica, devuelve solo metadatos
        if not data and 'page' not in self.request.query_params:
            total_items = self.queryset.count()
            page_size = self.get_page_size(self.request)
            total_pages = math.ceil(total_items / float(page_size)) if page_size else 0
            return Response({
                'total_items': total_items,
                'page_size': page_size,
                'total_pages': total_pages
            })

        # En otro caso, devuelve la respuesta paginada estándar
        return super().get_paginated_response(data)
