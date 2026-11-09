
from datetime import datetime
from typing import List, TYPE_CHECKING
from calendar import monthrange

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from rest_framework.exceptions import ValidationError
from kind.custom_fields.coords_field import CoordsJSONField

from kind.custom_fields.zone_periodicity_rules_field import ZonePeriodicityRulesJSONField
from kind.customauth.models.mixins import AssignableMixin
from kind.generics.models.base_model import CustomModelAbstract
# from kind.inventory.mixins.price_list_mixin import PriceListMixin

if TYPE_CHECKING:
    from kind.zones.models import Polygon


def _tdt(date: str) -> datetime:
    """
    To datetime: Converts a "%Y-%m-%d" str date to a datetime object
    """

    if type(date) == str:
        return datetime.strptime(date, "%Y-%m-%d")
    return date


def _tsd(date: datetime) -> str:
    """
    To string date: Converts a datetime object to a "%Y-%m-%d" str date
    """

    if type(date) == str:
        return date
    return date.strftime("%Y-%m-%d")


def _is_date_in_valid_month_days(date_obj: datetime, valid_days: list):
    """
    Check if the day of a given datetime object is in the provided list of valid days.
    Handles negative values where -1 is the last day of the month, -2 is the second to last, etc.

    :param date_obj: Datetime object representing the date to check
    :param valid_days: List of integers representing valid days (1-31 and negative values for last days of the month)
    :return: True if the day of date_obj is in the list of valid_days, False otherwise
    """
    # Extract the day and the total number of days in the month
    day_of_month = date_obj.day
    total_days_in_month = monthrange(date_obj.year, date_obj.month)[1]

    # Adjust negative values to match the actual day of the month
    adjusted_valid_days = [day if day > 0 else total_days_in_month + day + 1 for day in valid_days]

    # Check if the day is in the list of adjusted valid days
    return day_of_month in adjusted_valid_days


def _is_date_in_valid_year_weeks(date_obj: datetime, valid_weeks: list):
    """
    Check if the week of the month of a given datetime object is in the provided list of valid weeks.
    Handles negative values where -1 is the last week of the month, -2 is the second to last, etc.

    :param date_obj: Datetime object representing the date to check
    :param valid_weeks: List of integers representing valid weeks (1, 2, 3, 4, -1 for the last week, etc.)
    :return: True if the week of the month of date_obj is in the list of valid_weeks, False otherwise
    """
    # Calculate the week of the month
    # first_day_of_month = date_obj.replace(day=1)
    week_of_month = (date_obj.day - 1) // 7 + 1

    # Find the total number of weeks in the month
    total_days_in_month = monthrange(date_obj.year, date_obj.month)[1]
    last_day_of_month = date_obj.replace(day=total_days_in_month)
    total_weeks_in_month = (last_day_of_month.day - 1) // 7 + 1

    # Adjust negative values to match the actual week of the month
    adjusted_valid_weeks = [week if week > 0 else total_weeks_in_month + week + 1 for week in valid_weeks]

    # Check if the week of the month is in the list of adjusted valid weeks
    return week_of_month in adjusted_valid_weeks


def _is_date_in_valid_ranges(date_obj: datetime, date_ranges: list):
    return any(
        _tdt(start_date).date() <= _tdt(date_obj).date() <= _tdt(end_date).date()
        for start_date, end_date in date_ranges
    )


class Zone(CustomModelAbstract, AssignableMixin):
    auto_id = models.BigIntegerField(default=0)
    label = models.CharField(max_length=510)
    polygons: models.Manager
    # users = models.ManyToManyField(
    #     'customauth.User',
    #     blank=True,
    #     related_name='zones',
    # )
    # sales_points = models.ManyToManyField(
    #     'inventory.SalesPoint',
    #     blank=True,
    #     related_name='zones',
    # )
    zone_periodicity_rules: dict = ZonePeriodicityRulesJSONField(
        default=dict, blank=True, null=True
    )
    task_template = models.ForeignKey(
        'tasks.StatusFlowTemplate',
        null=True,
        blank=True,
        related_name='zones',
        on_delete=models.SET_NULL,
    )
    additional_addresses = models.ManyToManyField(
        'addresses.Address',
        blank=True,
        related_name='additionals_in_zones',
    )
    excluded_addresses = models.ManyToManyField(
        'addresses.Address',
        blank=True,
        related_name='excluded_in_zones',
    )
    coords = CoordsJSONField(default=None, blank=True, null=True)

    """
    # zone_periodicity_rules(date)
    # names: ever | dates | ranges | week-days | months | month-days | month-weeks | years | year-days | year-weeks | year-months
    {
        "asociation": "AND", # "OR"
        "rules": [
            {
                "type": "weekday",
                "values": [1, 2]
            },
            {
                "type": "monthweek",
                "values": [1, 3, 5]
            },
            {
                "values": [1, 3, 5]
            },
            {
                "name": "between",
                "type": "range",
                "values": ["2024/01/01", "2024/01/03"]
            },
            {
                "name": "thisTwo",
                "type": "dates",
                "values": ["2024/01/01", "2024/01/02", "2024/01/03"]
            },
            {
                "name": "custom",
                "type": "code",
                "values": ["(zone) => [1, 2].includes(new Date().weekday())"]
            }
        ]
    }
    """

    def is_available_at_date(self, date: str = None):

        # class AvailableDateTypes:
        #     ever = 'ever'
        #     dates = 'dates'
        #     ranges = 'ranges'
        #     weekdays = 'weekdays'
        #     months = 'months'
        #     monthdays = 'monthdays'
        #     monthweeks = 'monthweeks'
        #     years = 'years'
        #     yeardays = 'yeardays'
        #     yearweeks = 'yearweeks'
        #     yearmonths = 'yearmonths'

        validators = {
            "ever": lambda date, values: True,
            "dates": lambda date, values: _tsd(date) in values,
            "ranges": _is_date_in_valid_ranges,
            "weekdays": lambda date, values: (_tdt(date).weekday() + 1) in values,
            "months": lambda date, values: _tdt(date).month in values,
            "monthdays": _is_date_in_valid_month_days,
            "monthweeks": _is_date_in_valid_year_weeks,
            "years": lambda date, values: _tdt(date).year in [year if year >= 0 else datetime.now().year + year for year in values],
        }

        if not self.zone_periodicity_rules:
            return False

        rules: List[dict] = self.zone_periodicity_rules.get('rules')
        results = []

        for rule in rules:
            rule_type = rule.get('type')
            rule_values = rule.get('values')
            validator_fn = validators.get(rule_type, None)
            if validator_fn is None:
                raise ValidationError({"error": f"{rule_type} is not a valid rule type."})
            results.append(validator_fn(date or datetime.now(), rule_values))

        asociation = self.zone_periodicity_rules.get('asociation')

        return all(results) if asociation == 'and' else any(results)

    @property
    def is_available_today(self):
        return self.is_available_at_date()

    @property
    def center(self):
        poly_count = self.polygons.count()
        if not self.polygons or poly_count == 0:
            return None

        sum_lat, sum_lng = 0, 0
        poly_count = 0
        for polygon in self.polygons.all():
            polygon: 'Polygon'
            if not polygon.center:
                continue
            poly_count += 1
            lat = polygon.center[0]
            lng = polygon.center[1]
            sum_lat += lat
            sum_lng += lng

        mid_lat = sum_lat / (poly_count or 1)
        mid_lng = sum_lng / (poly_count or 1)

        return [mid_lat, mid_lng]

    def set_coords_to_center(self):
        center = self.center
        self.coords = {"latlng": center} if center else None
        self.save()

    def save(self, *args, **kwargs):
        if self._state.adding:
            # SET AUTO ID
            self.auto_id = self.company.zones_auto_enumeration + 1
            self.company.zones_auto_enumeration = self.auto_id
            self.company.save()
            # SET DEFAULT PERIODICITY RULES
            self.zone_periodicity_rules = {
                "asociation": 'and',
                "rules": [
                    {
                        "type": "ever",
                        "values": []
                    }
                ]
            }

        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.label

    class Meta:
        ordering = ["-created_at"]


# @receiver(m2m_changed, sender=Zone.polygons.through)
# def polygons_changed(sender, instance: Zone, action, pk_set, **kwargs):
#     instance.coords = {
#         "latlng": instance.center
#     } if instance.center else None
