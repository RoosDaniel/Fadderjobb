from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings

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

    def url(self):
        return settings.DEFAULT_DOMAIN + \
               reverse("trade:complete", kwargs={"sender_username": self.sender.username})

    def notify_receiver(self):
        message = "Du har mottagit en bytesförfrågan från {username}.\n\nSe bytet här: {url}"\
            .format(username=self.sender.username, url=self.url())

        send_mail(self.receiver.email, "Bytesförfrågan", message=message)

    def apply(self, accepted):
        if accepted:
            self.completed = True
        else:
            pass

        self.save()

    @staticmethod
    def get_active(sender, receiver):
        return Trade.objects.get(sender=sender, receiver=receiver, completed=False)
