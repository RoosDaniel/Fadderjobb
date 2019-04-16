from django.db import models
from django.utils import timezone
from django.urls import reverse

from fadderjobb.staben_mail import send_mail


class Trade(models.Model):
    created = models.DateTimeField(default=timezone.now)
    completed = models.BooleanField(default=False)

    sender = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="sent_trades")
    receiver = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="received_trades")

    sent = models.ManyToManyField("fadderanmalan.JobUser", related_name="sent_in_trades")
    requested = models.ManyToManyField("fadderanmalan.JobUser", related_name="requested_in_trades")

    def __str__(self):
        return "%s -> %s" % (self.sender, self.receiver)

    def notify_receiver(self):
        message = """Du har mottagit en bytesförfrågan från {username}.
Se bytet här: {trade_url}""".format(
            username=self.sender.username,
            trade_url=reverse("trade:complete", **{"sender": self.sender.username}))

        send_mail(self.receiver.email, "Bytesförfrågan", message=message)

    def apply(self):
        self.completed = True

        self.save()
