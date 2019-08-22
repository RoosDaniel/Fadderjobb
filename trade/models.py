from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings

from fadderjobb.utils import notify_user, notify_group

from fadderanmalan.models import JobUser


class Trade(models.Model):
    created = models.DateTimeField(default=timezone.now)
    completed = models.BooleanField(default=False)

    sender = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="sent_trades")
    receiver = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="received_trades")

    sent = models.ManyToManyField("fadderanmalan.Job", related_name="sent_in_trades", blank=True)
    requested = models.ManyToManyField("fadderanmalan.Job", related_name="requested_in_trades", blank=True)

    def __str__(self):
        return "%s -> %s" % (self.sender, self.receiver)

    def url(self):
        return settings.DEFAULT_DOMAIN + \
               reverse("trade:see", args=[self.sender.username])

    def notify_receiver(self):
        notify_user(self.receiver, template="trade_received", template_context=dict(
            sender=self.sender, trade_url=self.url()
        ))

    def accept(self):
        # A Trade needs to be marked as completed before adding and removing of JobUsers since we don't want
        # to delete completed trades. (The deletion function in signals.py won't delete completed Trades.)
        self.completed = True
        self.save()

        # These need to be created before adding and removing JobUsers since the signal-listeners
        # will start removing them right away.
        receiver_gets = self.sent.all()
        sender_gets = self.requested.all()

        # We need to create new instances instead of updating the old ones in order to
        # trigger the signal for removing all other trades concerning these job-user combinations.
        for job in receiver_gets:
            JobUser.create(job=job, user=self.receiver)
            JobUser.remove(job=job, user=self.sender)
        for job in sender_gets:
            JobUser.create(job=job, user=self.sender)
            JobUser.remove(job=job, user=self.receiver)

        notify_user(self.sender, template="trade_accepted", template_context=dict(
            receiver=self.receiver
        ))

        notify_group("JobSwapNotifications", template="admin_jobs_traded", template_context=dict(
            sender=self.sender,
            receiver=self.receiver,
            receiver_gets=receiver_gets,
            sender_gets=sender_gets,
        ))

    def deny(self):
        self.delete()

        notify_user(self.sender, template="trade_denied", template_context=dict(
                        receiver=self.receiver
                    ))

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
