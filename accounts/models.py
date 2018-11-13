from django.db import models

from django.contrib.auth.models import AbstractUser, UserManager


class _UserManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})


class User(AbstractUser):
    objects = _UserManager()

    def points(self):
        return sum(job.points for job in self.jobs.all())
