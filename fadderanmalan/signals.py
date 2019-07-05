from django.dispatch import receiver
from django.db.models.signals import pre_delete, post_save
from django.db.models import Q

from fadderanmalan.models import JobUser, LeaveQueue, EnterQueue, ActionLog
from trade.models import Trade


def _delete_trades(job_user: JobUser):
    Trade.objects\
        .filter(Q(sender=job_user.user) | Q(receiver=job_user.user))\
        .filter(Q(sent=job_user.job) | Q(requested=job_user.job))\
        .exclude(completed=True)\
        .delete()


def _delete_LQ(job_user):
    LeaveQueue.objects.filter(job=job_user.job, user=job_user.user).delete()


def _delete_EQ(job_user):
    EnterQueue.objects.filter(job=job_user.job, user=job_user.user).delete()


@receiver(post_save, sender=JobUser)
def on_registration(sender, instance: JobUser, created, **kwargs):
    if not created:
        return

    log = ActionLog(job=instance.job, user=instance.user, type=ActionLog.TYPES.REGISTRATION_CREATE.value)
    log.save()

    _delete_trades(instance)
    _delete_LQ(instance)  # Technically impossible, but you never know
    _delete_EQ(instance)


@receiver(pre_delete, sender=JobUser)
def on_deregistration(sender, instance: JobUser, **kwargs):
    log = ActionLog(job=instance.job, user=instance.user, type=ActionLog.TYPES.REGISTRATION_DELETE.value)
    log.save()

    _delete_trades(instance)
    _delete_LQ(instance)
    _delete_EQ(instance)  # Technically impossible, but you never know


@receiver(post_save, sender=EnterQueue)
def on_create_eq(sender, instance: EnterQueue, created, **kwargs):
    if not created:
        return

    log = ActionLog(job=instance.job, user=instance.user, type=ActionLog.TYPES.ENTER_QUEUE_CREATE.value)
    log.save()


@receiver(pre_delete, sender=EnterQueue)
def on_delete_eq(sender, instance: EnterQueue, **kwargs):
    log = ActionLog(job=instance.job, user=instance.user, type=ActionLog.TYPES.ENTER_QUEUE_DELETE.value)
    log.save()


@receiver(post_save, sender=LeaveQueue)
def on_create_lq(sender, instance: LeaveQueue, created, **kwargs):
    if not created:
        return

    log = ActionLog(job=instance.job, user=instance.user, type=ActionLog.TYPES.LEAVE_QUEUE_CREATE.value)
    log.save()


@receiver(pre_delete, sender=LeaveQueue)
def on_delete_lq(sender, instance: LeaveQueue, **kwargs):
    log = ActionLog(job=instance.job, user=instance.user, type=ActionLog.TYPES.LEAVE_QUEUE_DELETE.value)
    log.save()
