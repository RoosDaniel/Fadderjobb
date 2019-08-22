from django.dispatch import receiver
from django.db.models.signals import pre_delete, post_save, post_delete
from django.db.models import Q

from fadderanmalan.models import JobUser, EnterQueue, ActionLog
from trade.models import Trade
import accounts.utils

from fadderjobb.utils import notify_user


def _delete_trades(job_user: JobUser):
    Trade.objects\
        .filter(Q(sender=job_user.user) | Q(receiver=job_user.user))\
        .filter(Q(sent=job_user.job) | Q(requested=job_user.job))\
        .exclude(completed=True)\
        .delete()


def _delete_EQ(job_user):
    EnterQueue.objects.filter(job=job_user.job, user=job_user.user).delete()


@receiver(post_save, sender=JobUser)
def post_registration(sender, instance: JobUser, created, **kwargs):
    if not created:
        return

    log = ActionLog(job=instance.job, user=instance.user, type=ActionLog.TYPES.REGISTRATION_CREATE.value)
    log.save()

    notify_user(instance.user, template="job_registration", template_context=dict(
        job=instance.job,
        user=instance.user
    ))

    instance.user.update_points()
    accounts.utils.update_user_placings()

    _delete_trades(instance)
    _delete_EQ(instance)


@receiver(pre_delete, sender=JobUser)
def pre_deregistration(sender, instance: JobUser, **kwargs):
    log = ActionLog(job=instance.job, user=instance.user, type=ActionLog.TYPES.REGISTRATION_DELETE.value)
    log.save()

    _delete_trades(instance)
    _delete_EQ(instance)  # Technically impossible, but you never know


@receiver(post_delete, sender=JobUser)
def post_deregistration(sender, instance: JobUser, **kwargs):
    instance.user.update_points()
    accounts.utils.update_user_placings()


@receiver(post_save, sender=EnterQueue)
def post_create_eq(sender, instance: EnterQueue, created, **kwargs):
    if not created:
        return

    log = ActionLog(job=instance.job, user=instance.user, type=ActionLog.TYPES.ENTER_QUEUE_CREATE.value)
    log.save()


@receiver(pre_delete, sender=EnterQueue)
def pre_delete_eq(sender, instance: EnterQueue, **kwargs):
    log = ActionLog(job=instance.job, user=instance.user, type=ActionLog.TYPES.ENTER_QUEUE_DELETE.value)
    log.save()
