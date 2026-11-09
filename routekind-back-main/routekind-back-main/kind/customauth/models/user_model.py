
import re
import string
from typing import TYPE_CHECKING, List
from datetime import timedelta

from django.db import models
from django.core import validators
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser
from rest_framework.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.utils import timezone


from kind.custom_fields.coords_field import CoordsJSONField
from kind.customauth.managers.user_manager import UserManager
from kind.customauth.models.auth_token_model import AUTH_TOKEN_API
from kind.customauth.models.mixins import UserRoleMixin
from kind.zones.models import Polygon
from kind.generics.models import GenericBaseModel
from kind.customauth.models.temporal_password_model import TemporalPassword
from kind.generics.utils import has_consecutive_charactes, has_consecutive_numbers
from kind.generics.utils import get_password_salt_from_username

from encrypted_model_fields.fields import EncryptedEmailField, EncryptedCharField

if TYPE_CHECKING:
    from kind.inventory.models import SalesPoint
    from kind.companies.models import Company
    from kind.connections.models import ApiConnection

ATTEMPTS_TO_BLOCK = 5
PASSWORD_EXPIRATION_DELTA_TIME = {"days": 45}


class CustomUsernameValidator(validators.RegexValidator):
    regex = r'^[\w.]+\Z'
    message = _(
        'El nombre de usuario no es válido.'
    )
    flags = re.ASCII


class CoordsHistoryMixin(models.Model):
    COORDS_FIELD_NAME = "coords"
    coords_history: List[dict] = models.JSONField(default=list, blank=True)

    def save(self, *args, **kwargs):

        current_coords: dict = getattr(self, CoordsHistoryMixin.COORDS_FIELD_NAME)
        if current_coords:
            prev_coords: dict = self.__class__.objects \
                .filter(id=self.id) \
                .values_list('coords', flat=True)[0]
            prev_latlng = prev_coords.get('latlng') if prev_coords else None
            if prev_latlng:
                next_latlng = current_coords.get('latlng')

                if (
                    not next_latlng or
                    prev_latlng[0] != next_latlng[0] or
                    prev_latlng[1] != next_latlng[1]
                ):
                    self.coords_history.append(prev_coords)

        return super().save(*args, **kwargs)

    class Meta:
        abstract = True


class User(
    GenericBaseModel,
    AbstractBaseUser,
    UserRoleMixin,
    CoordsHistoryMixin
):
    app_name = 'users'
    username_validator = CustomUsernameValidator()
    auto_id = models.BigIntegerField(default=0)
    password_history = models.JSONField(default=list, blank=True)
    login_password_error_attempts = models.IntegerField(default=0)
    temporal_user_block_datetime = models.DateTimeField(null=True, blank=True)
    password_creation_datetime = models.DateTimeField(default=timezone.now)

    @property
    def is_blocked(self):
        if self.login_password_error_attempts >= ATTEMPTS_TO_BLOCK:
            unlock_datetime = self.temporal_user_block_datetime + timedelta(minutes=5)
            if timezone.now() <= unlock_datetime:
                return True
            else:
                # User is not more blocked
                self.reset_login_password_error_attempts()

        return False

    def register_login_password_error_attempt(self):
        if self.login_password_error_attempts < ATTEMPTS_TO_BLOCK:
            self.login_password_error_attempts += 1
            self.temporal_user_block_datetime = timezone.now()
            self.save()

    def reset_login_password_error_attempts(self):
        self.login_password_error_attempts = 0
        self.temporal_user_block_datetime = None
        self.save()

    username = models.CharField(
        _("username"),
        max_length=60,
        unique=True,
        help_text=_(
            _("Required. 60 characters or fewer. Letters, digits and @/./+/-/_ only.")
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    name = EncryptedCharField(
        _("name"),
        max_length=60,
        null=True,
        blank=True,
        default='',
    )
    email = EncryptedEmailField(
        _("email address"),
        max_length=255,
        default=None,
        null=True,
        blank=True,
        # unique=True
        # TODO: Unique per company?
    )
    is_admin = models.BooleanField(
        _("admin status"),
        default=False,
        help_text=_(
            _("Designates that this user has access to the django admin panel")
        ),
    )
    is_superuser = models.BooleanField(
        _("superuser status"),
        default=False,
        help_text=_(
            _("Designates that this user has all permissions without explicitly assigning them.")
        ),
    )
    created_by: 'User' = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='%(app_label)s_%(class)s_create_user'
    )
    updated_by: 'User' = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='%(app_label)s_%(class)s_update_user'
    )
    assigned_sales_point: 'SalesPoint' = models.ForeignKey(
        'inventory.SalesPoint',
        related_name='users',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    last_activity_date = models.DateTimeField(null=True, blank=True)
    require_change_password_at_first_login_completed = models.BooleanField(default=False)
    temporal_password_setup_date = models.DateTimeField(null=True, blank=True)
    track_coords = models.BooleanField(default=True)
    coords = CoordsJSONField(default=None, null=True, blank=True)
    roles: models.Manager
    jwt_auth_tokens: models.Manager
    connection: 'ApiConnection'
    temporal_password_records: models.Manager
    zones_zone_assigned_users: models.Manager  # Assigned zones from zones AssignableMixin
    tasks_task_assigned_users: models.Manager  # Assigned tasks from tasks AssignableMixin

    @property
    def assigned_tasks(self):
        return self.tasks_task_assigned_users

    @property
    def assigned_zones(self):
        return self.zones_zone_assigned_users

    @property
    def password_expires(self):
        # Calcula la fecha de expiración agregando los días de expiración a la fecha de creación
        expiration_date = self.password_creation_datetime + timedelta(**PASSWORD_EXPIRATION_DELTA_TIME)
        if expiration_date <= timezone.now():
            return True

        if not self.require_change_password_at_first_login_completed:
            return False

        return self.temporal_password_setup_date

    def set_temporal_password(self, password, *, setted_by):
        current_temporal_password: 'TemporalPassword' = self.temporal_password_records.filter(
            approved_by__isnull=True).first()
        if current_temporal_password is None:
            raise ValidationError({'error': 'There is not pending password request to approve'})
        current_temporal_password.approve(password, setted_by)

    def is_connection_request(self, request, *, raise_exception=False):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            access = auth_header.split(' ')[1]
            token_exists_and_is_valid = self.jwt_auth_tokens.filter(
                access=access,
                type=AUTH_TOKEN_API
            )
            if token_exists_and_is_valid:
                return True

        if raise_exception:
            return ValidationError({"error": "An API connection token is required."})

        return False

    def get_assigned_addresses(self, all_addresses_qs: models.QuerySet):
        result_addresses = all_addresses_qs.none()

        # FROM ZONES
        zones: models.Manager = self.assigned_zones
        polygons_ids = [
            str(id) for id in zones.values_list('polygons', flat=True) if id
        ]

        for polygon in Polygon.objects.filter(id__in=polygons_ids):
            polygon: 'Polygon'
            if polygon.is_available_today:
                polygon_internal_addresses = polygon.get_internal_addresses(all_addresses_qs)
                if polygon_internal_addresses and polygon_internal_addresses.count() > 0:
                    result_addresses |= polygon_internal_addresses

        # FROM TASKS
        tasks: models.Manager = self.assigned_tasks
        tasks_addresses_id = tasks.values_list('contact_address', flat=True)
        result_addresses |= all_addresses_qs.filter(id__in=tasks_addresses_id)

        # RESULT RESULT
        return result_addresses

    @property
    def is_staff(self):
        "Is the user a member of staff (can access django admin)?"
        return self.is_admin

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["email"]

    module_name = 'users'

    # def set_temporal_password(self, password, *, expiry_date=None):
    #     if self.get_temporal_password() is not None:
    #         raise ValidationError({ 'error': 'Temporal password already created' })

    #     self.set_password(password)
    #     temporal_password_record = TemporalPassword.objects.create(
    #         user=self,
    #         expiry_date=expiry_date or timezone.now() + timedelta(days=1),
    #         password=self.password,
    #     )

    @property
    def current_temporal_password(self) -> 'TemporalPassword':
        return self.temporal_password_records.filter(complete_date__isnull=True).order_by("-created_at").first()

    def create_temporal_password_request(self, *, created_by: 'User' = None):
        return TemporalPassword.create_request(user=self, created_by=created_by)

    # def has_temporal_password_and_expired(self):
    #     temporal_password_record: 'TemporalPassword' = self.get_temporal_password()
    #     if temporal_password_record is None:
    #         return False

    #     return timezone.now() > temporal_password_record.expiry_date

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def has_perm(self, perm_list, *, raise_exception=False):
        # Django admin only
        return self.is_active and self.is_admin

    def has_module_perms(self, perms) -> bool:
        # Django admin only
        return self.is_active and self.is_admin

    def _validate_allow_more_users(self):
        company: 'Company' = self.company

        no_more_users_allowed_exception = ValidationError({'error': 'No more users allowed for this company.'})

        if self._state.adding:
            if not company.allow_more_users:
                raise no_more_users_allowed_exception

        else:
            prev_is_active = self.__class__.objects.filter(id=self.id).values_list('is_active', flat=True)[0]
            new_is_active = self.is_active
            if not prev_is_active and new_is_active and not company.allow_more_users:
                raise no_more_users_allowed_exception

    def _validate_password(self, password: str):
        # Verificar la longitud mínima de la contraseña
        if len(password) < 12:
            raise ValidationError({"password": "La contraseña es muy corta, debe contener al menos 12 carácteres."})

        # Verificar que contenga al menos una letra minúscula
        if not re.search("[a-z]", password):
            raise ValidationError({"password": "La contraseña debe contener al menos 1 letra en minúsculas."})

        # Verificar que contenga al menos una letra mayúscula
        if not re.search("[A-Z]", password):
            raise ValidationError({"password": "La contraseña debe contener al menos 1 letra en mayusculas."})

        # Contar caracteres numéricos
        count_digit = sum(c.isdigit() for c in password)
        if count_digit < 1:
            raise ValidationError({"password": "La contraseña debe contener al menos 1 caracteres numéricos."})

        # Contar caracteres especiales
        count_special = sum(c in string.punctuation for c in password)
        if count_special < 1:
            raise ValidationError({"password": "La contraseña debe contener al menos 1 caracter especial."})

        # No permitir caracteres consecutivos
        if has_consecutive_charactes(password):
            raise ValidationError(
                {"password": "No están permitidos los carácteres consecutivos (ABC, etc)."})

        # No permitir números consecutivos
        if has_consecutive_numbers(password):
            raise ValidationError(
                {"password": "No están permitidos los números consecutivos (123, etc)."})

        # La contraseña no debe ser igual al usuario
        if password == self.username:
            raise ValidationError({"password": "La contraseña no puede ser igual al nombre de usuario."})

        # Verificar el historial de contraseñas
        salt = get_password_salt_from_username(self.username)
        maked_password = make_password(password, salt=salt)
        if maked_password in self.password_history:
            raise ValidationError(
                {"password": "No es posible establecer contreseñas que ya fueron utilizadas previemente."})

        return True

    def add_password_history(self, password: str):
        if password not in self.password_history:
            self.password_history = [*self.password_history, password]

    def set_valid_password(self, raw_password: str):
        self.add_password_history(self.password)
        self._validate_password(raw_password)
        self.set_password(raw_password)
        salt = get_password_salt_from_username(self.username)
        self.add_password_history(make_password(raw_password, salt=salt))
        self.password_creation_datetime = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.username} ({self.company.name})"

    def save(self, *args, **kwargs):
        self._validate_allow_more_users()

        # Set auto_id on create
        if self._state.adding:
            self.company.users_auto_enumeration += 1
            self.auto_id = self.company.users_auto_enumeration
            self.company.save()

        return super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("user")
        verbose_name_plural = _("users")
