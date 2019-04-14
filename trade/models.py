from django.db import models
from django.utils import timezone


class Trade(models.Model):
    created = models.DateTimeField(default=timezone.now)

    sent = models.ManyToManyField("fadderanmalan.JobUser", related_name="sent_in_trades")
    requested = models.ManyToManyField("fadderanmalan.JobUser", related_name="requested_in_trades")
