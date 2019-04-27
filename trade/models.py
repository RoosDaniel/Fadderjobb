from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings

from fadderjobb.staben_mail import send_mail

from fadderanmalan.models import JobUser


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
               reverse("trade:see", args=[self.sender.username])

    def notify_receiver(self):
        message = "Du har mottagit en bytesförfrågan från {username}.\n\nSe bytet här: {url}"\
            .format(username=self.sender.username, url=self.url())

        send_mail(self.receiver.email, "Bytesförfrågan", message)

    def accept(self):
        subject = "Ett byte har gått igenom"
        message = "{username} har accepterat ditt byte!" \
            .format(username=self.receiver.username)

        # We need to create new instances instead of updating the old ones in order to
        # trigger the signal for removing all other trades concerning these job-user combinations.
        for job_user in self.sent.all():
            JobUser.create(job=job_user.job, user=self.receiver)
        for job_user in self.requested.all():
            JobUser.create(job=job_user.job, user=self.sender)

        # A problem with this is that there is no point in saving the Trade since
        # all its M2M relations will have been removed
        # TODO Find a way to save info about a Trade that doesn't rely on JobUser instances
        self.sent.delete()
        self.requested.delete()

        self.completed = True
        self.save()

        send_mail(self.sender.email, subject, message)

    def deny(self):
        subject = "Ett byte har avslagits"
        message = "{username} har tackat nej till ditt byte." \
            .format(username=self.receiver.username)

        self.delete()

        send_mail(self.sender.email, subject, message)

    def cancel(self):
        self.delete()

    @staticmethod
    def get_active(sender, receiver):
        return Trade.objects.get(sender=sender, receiver=receiver, completed=False)

    @staticmethod
    def get_trade(user_1, user_2):
        try:
            return Trade.get_active(user_1, user_2)
        except Trade.DoesNotExist:
            return Trade.get_active(user_2, user_1)
