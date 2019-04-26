from django.dispatch import receiver
from django.db.models.signals import pre_delete, post_save
from django.db.models import Q

from fadderanmalan.models import JobUser
from trade.models import Trade


def _delete_trades(job_user):
    Trade.objects\
        .filter(Q(sender=job_user.user) | Q(receiver=job_user.user))\
        .filter(Q(sent__job=job_user.job) | Q(requested__job=job_user.job))\
        .delete()


@receiver(pre_delete, sender=JobUser)
def on_deregistration(sender, instance, **kwargs):
    _delete_trades(instance)


@receiver(post_save, sender=JobUser)
def on_registration(sender, instance, created, **kwargs):
    if not created:
        return

    _delete_trades(job_user)
