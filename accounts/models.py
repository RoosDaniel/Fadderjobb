from datetime import datetime

from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.sessions.models import Session

from phonenumber_field.modelfields import PhoneNumberField


class _UserManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})


class User(AbstractUser):
    objects = _UserManager()

    motto = models.TextField(max_length=100, blank=True)
    phone_number = PhoneNumberField(blank=True, null=True)

    def points(self):
        return self.jobs.all().aggregate(Sum("points"))["points__sum"] or 0

    def can_register(self):
        return self.is_authenticated and self.phone_number is not None
