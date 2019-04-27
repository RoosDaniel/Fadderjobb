from django.dispatch import receiver
from django.db.models.signals import pre_delete, post_save
from django.db.models import Q

from fadderanmalan.models import JobUser, LeaveQueue, EnterQueue
from trade.models import Trade


def _delete_trades(job_user):
    Trade.objects\
        .filter(Q(sender=job_user.user) | Q(receiver=job_user.user))\
        .filter(Q(sent__job=job_user.job) | Q(requested__job=job_user.job))\
        .delete()


def _delete_LQ(job_user):
    LeaveQueue.objects.filter(job=job_user.job, user=job_user.user).delete()


def _delete_EQ(job_user):
    EnterQueue.objects.filter(job=job_user.job, user=job_user.user).delete()


@receiver(pre_delete, sender=JobUser)
def on_deregistration(sender, instance, **kwargs):
    _delete_trades(instance)
    _delete_LQ(instance)
    _delete_EQ(instance)  # Technically impossible, but you never know


@receiver(post_save, sender=JobUser)
def on_registration(sender, instance, created, **kwargs):
    if not created:
        return

    _delete_trades(instance)
    _delete_LQ(instance)  # Technically impossible, but you never know
    _delete_EQ(instance)
