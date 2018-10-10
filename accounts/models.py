from django.db import models

from django.contrib.auth.models import User


class Fadder(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="fadder")

    def __str__(self):
        return self.user.username

    def points(self):
        return sum(job.points for job in self.jobs.all())
