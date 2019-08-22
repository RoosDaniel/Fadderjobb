from datetime import datetime

from django.conf import settings
from django.shortcuts import reverse
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
    name = models.CharField(max_length=100, blank=True, null=True)
    read_guide = models.BooleanField(default=False)

    points = models.IntegerField(default=0)
    placing = models.IntegerField(blank=True, null=True)

    def __str__(self):
        if self.name:
            return "%s (%s)" % (self.name, self.username)
        return self.username

    def update_points(self):
        self.points = self.jobs.all().aggregate(Sum("points"))["points__sum"] or 0
        self.save()

    def can_register(self):
        if self.is_superuser or self.is_staff:
            return True

        return self.is_authenticated and self.phone_number is not None and self.read_guide

    def get_active_received_trades(self):
        return self.received_trades.filter(completed=False).all()

    def get_active_sent_trades(self):
        return self.sent_trades.filter(completed=False).all()

    def local_url(self):
        if not self.username:
            return None
        return reverse("accounts:profile", args=[self.username])

    def url(self):
        local_url = self.local_url()

        if not local_url:
            return None
        return settings.DEFAULT_DOMAIN + local_url
