from datetime import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.sessions.models import Session


class _UserManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})


class User(AbstractUser):
    objects = _UserManager()

    motto = models.TextField(max_length=100)

    def points(self):
        return sum(job.points for job in self.jobs.all())
