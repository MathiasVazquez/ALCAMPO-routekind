from typing import List, TYPE_CHECKING

from django.db import models
from rest_framework.exceptions import ValidationError

from kind.generics.models.base_model import CustomModelAbstract
# from kind.addresses.models import Address
# from kind.inventory.mixins.price_list_mixin import PriceListMixin

if TYPE_CHECKING:
    from kind.zones.models import Zone


def is_latlng_in_polygon(latlng: List[float], polygon: List[List[float]]):
    x, y = latlng
    n = len(polygon)
    is_inside = False

    j = n - 1
    for i in range(0, n):
        xi, yi = polygon[i]
        xj, yj = polygon[j]

        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
            is_inside = not is_inside
        j = i

    return is_inside


class Polygon(CustomModelAbstract):
    auto_id = models.BigIntegerField(default=0)
    zone: 'Zone' = models.ForeignKey(
        'zones.Zone',
        on_delete=models.CASCADE,
        related_name='polygons',
    )
    label = models.CharField(default="", blank=True, max_length=120)
    vertices = models.JSONField(default=list, blank=True)
    bounds = models.JSONField(default=list, blank=True)

    @property
    def _is_valid_vertices(self):
        return self.vertices and len(self.vertices) >= 3

    @property
    def center(self):
        if not self.bounds:
            return None

        sum_lat, sum_lng = 0, 0
        for lat, lng in self.bounds:
            sum_lat += lat
            sum_lng += lng

        mid_lat = sum_lat / len(self.bounds)
        mid_lng = sum_lng / len(self.bounds)

        return [mid_lat, mid_lng]

    def set_bounds(self):
        if not self._is_valid_vertices:
            self.bounds = []
            return

        # Inicializar los valores de latitud y longitud con valores extremos
        lat_min, lng_min = float('inf'), float('inf')
        lat_max, lng_max = float('-inf'), float('-inf')

        # Iterar sobre cada coordenada para encontrar los valores máximos y mínimos
        for lat, lng in self.vertices:
            lat_min = min(lat_min, lat)
            lng_min = min(lng_min, lng)
            lat_max = max(lat_max, lat)
            lng_max = max(lng_max, lng)

        # Los 'bounds' son los puntos extremos: [lat_min, lng_min], [lat_max, lng_max]
        self.bounds = [[lat_min, lng_min], [lat_max, lng_max]]

    def get_internal_addresses(self, addresses_qs: models.QuerySet):
        if not self._is_valid_vertices:
            return addresses_qs.none()

        if not self.bounds or len(self.bounds) == 0:
            self.set_bounds()

        in_bounds_addresses = addresses_qs.filter(
            company=self.company,
            coords__latlng__0__gt=self.bounds[0][0],
            coords__latlng__1__gt=self.bounds[0][1],
            coords__latlng__0__lt=self.bounds[1][0],
            coords__latlng__1__lt=self.bounds[1][1],
        )

        resolved_ids = []
        for address_id, latlng in in_bounds_addresses.values_list('id', 'coords__latlng'):
            if is_latlng_in_polygon(latlng, self.vertices):
                resolved_ids.append(str(address_id))

        return addresses_qs.filter(id__in=resolved_ids)

    def _validate_vertices(self):
        if type(self.vertices) != list:
            ValidationError({'vertices': 'This field must a list.'})

        if not all([
            type(v) == list and
            len(v) == 2 and
            type(v[0]) == float and
            type(v[1]) == float
            for v in self.vertices
        ]):
            ValidationError({'vertices': 'The list contains invalid values.'})

    @property
    def is_available_today(self):
        return self.zone.is_available_today

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.auto_id = self.company.polygons_auto_enumeration + 1
            self.company.polygons_auto_enumeration = self.auto_id
            self.company.save()

        self._validate_vertices()
        self.set_bounds()  # TODO: Only if vertices has change
        result = super().save(*args, **kwargs)
        self.zone.set_coords_to_center()
        return result

    def __str__(self) -> str:
        return str(self.id)
