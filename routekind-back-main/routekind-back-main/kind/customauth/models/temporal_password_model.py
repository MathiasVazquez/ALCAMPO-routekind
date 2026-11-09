
from typing import TYPE_CHECKING

from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from kind.generics.models import GenericBaseModel

if TYPE_CHECKING:
    from .user_model import User


class TemporalPassword(GenericBaseModel):
    user: 'User' = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name="temporal_password_records"
    )
    approved_by: 'User' = models.ForeignKey(
        'customauth.User',
        null=True,
        blank=True,
        related_name='temporal_password_approvedments',
        on_delete=models.SET_NULL,
    )
    approved_date = models.DateTimeField(null=True, blank=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    complete_date = models.DateTimeField(null=True, blank=True)
    password_hash = models.CharField(default=None, null=True, blank=True, max_length=250)

    @classmethod
    def create_request(self, user: 'User', *, created_by: 'User' = None):
        temporal_password = TemporalPassword(
            user=user,
            created_by=created_by or user,
            updated_by=created_by or user,
            company=user.company,
        )
        user.set_unusable_password()
        temporal_password.save()
        return temporal_password

    def approve(self, password: str, approved_by: 'User', *, expiry_date=None):
        # Validations
        if self.status != 'pending':
            raise ValidationError({'error': 'Temporal password already approved'})

        if approved_by.company.id != self.created_by.company.id or not approved_by.has_permission("users.update"):
            raise ValidationError({'error': 'You are not allowed to approve'})

        # Set new password
        self.created_by.require_change_password_at_first_login_completed = False
        self.created_by.set_valid_password(password)
        self.created_by.save()

        # Set new status
        self.approved_by = approved_by
        self.password_hash = self.created_by.password
        self.approved_date = timezone.now()
        self.expiry_date = expiry_date or self.approved_date + timedelta(
            hours=self.company.default_temporal_new_passwords_lifetime_hours
            # seconds=1,
        )
        self.save()

    def complete(self, password: str):
        if self.status == 'pending':
            raise ValidationError({'error': 'Temporal password is not approved yet'})

        if self.status == 'expired':
            raise ValidationError({'error': 'Temporal password is expired'})

        if self.status == 'completed':
            raise ValidationError({'error': 'Temporal password is completed'})

        self.user.set_valid_password(password)
        self.complete_date = timezone.now()
        self.save()

    @property
    def status_label(self):
        return {
            'completed': 'Completado',
            'expired': 'Expirado',
            'approved': 'Aprobado',
            'pending': 'Pendiente',
        }[self.status]

    @property
    def status(self):
        # Completed
        if self.complete_date is not None:
            return 'completed'

        # Expired
        if self.expiry_date and timezone.now() > self.expiry_date:
            return 'expired'

        # Approved
        if self.approved_by is not None:
            return 'approved'

        # Pending
        return 'pending'

    @property
    def has_expired(self):
        return self.status == 'expired'

    class Meta:
        verbose_name = _("Temporal password")
        verbose_name_plural = _("Temporal passwords")
