from collections import OrderedDict

import datetime

from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.urls import reverse
from django.db.models import Q
from django.core.exceptions import ValidationError

from constance import config

from fadderjobb.staben_mail import send_mail


class Type(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Equipment(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    size = models.CharField(max_length=10, null=True, blank=True, help_text="Frivillig storlek på utrustningen. "
                                                                            "Användbart för t.ex. t-shirts.")

    def __str__(self):
        if self.size != "":
            return "%s | %s" % (self.size, self.name)
        return self.name


class EquipmentOwnership(models.Model):
    dispensed_at = models.DateTimeField(default=timezone.now)
    returned = models.BooleanField(default=False)

    job = models.ForeignKey("Job", on_delete=models.SET_NULL, related_name="equipments",
                            null=True, blank=True, help_text="Vilket jobb gäller utdelningen? Kan vara tom. "
                                                             "Defaultar till senast skapade utdelningen.")

    equipment = models.ForeignKey("Equipment", on_delete=models.CASCADE, related_name="ownerships")
    fadder = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="equipments",
                               verbose_name="Fadder")

    def __str__(self):
        return "%s | %s" % (self.equipment, self.fadder)

    # Used in list_display in admin
    def name(self):
        return self.equipment.name

    def size(self):
        return self.equipment.size


class EnterQueue(models.Model):
    created = models.DateField(editable=False)

    job = models.ForeignKey("Job", on_delete=models.CASCADE, related_name="enter_queue")
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="enter_queue")

    def __str__(self):
        return " | ".join([self.job.name, self.user.username])

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()

        return super(self.__class__, self).save(*args, **kwargs)

    @classmethod
    def get_first(cls, job):
        res = cls.objects.filter(job=job).order_by("created").first()

        if res is None:
            raise cls.DoesNotExist

        return res

    def apply(self):
        self.job.users.add(self.user)
        self.delete()
        self.job.save()

        send_mail(self.user.email, "Du har fått en plats på ett jobb du har köat för",
                  "Du har fått en plats på jobbet '%s'. Se jobbet här: %s" % (self.job.name, self.job.url()))


class LeaveQueue(models.Model):
    created = models.DateField(editable=False)

    job = models.ForeignKey("Job", on_delete=models.CASCADE, related_name="leave_queue")
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="leave_queue")

    def __str__(self):
        return " | ".join([self.job.name, self.user.username])

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()

        return super(self.__class__, self).save(*args, **kwargs)

    @classmethod
    def get_first(cls, job):
        res = cls.objects.filter(job=job).order_by("created").first()

        if res is None:
            raise cls.DoesNotExist

        return res

    def apply(self):
        self.job.users.remove(self.user)
        self.delete()
        self.job.save()

        send_mail(self.user.email, "Någon har tagit en plats på ett jobb du vill lämna",
                  "Någon har tagit din plats på jobbet '%s'. Se jobbet här: %s" % (self.job.name, self.job.url()))


def default_locked_after():
    return config.DEFAULT_JOB_LOCKED_AFTER


def default_locked_until():
    return config.DEFAULT_JOB_LOCKED_UNTIL


def default_hidden_after():
    return config.DEFAULT_JOB_HIDDEN_AFTER


def default_hidden_until():
    return config.DEFAULT_JOB_HIDDEN_UNTIL


def default_start():
    return config.DEFAULT_JOB_TIME_START


def default_end():
    return config.DEFAULT_JOB_TIME_END


class Job(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(help_text="Vilket datum jobbet gäller.")

    start_time = models.TimeField(help_text="När jobbet ska börja.", default=default_start)
    end_time = models.TimeField(help_text="När jobbet ska sluta.", default=default_end)

    description = models.TextField(null=True, blank=True)
    points = models.IntegerField()
    slots = models.IntegerField()

    hidden = models.BooleanField(help_text="Om jobbet ska döljas från frontend:en. "
                                           "Överskrider datumen nedan")
    hidden_after = models.DateField(default=default_hidden_after,
                                    help_text="EFTER detta datum kommer jobbet att döljas.")
    hidden_until = models.DateField(default=default_hidden_until,
                                    help_text="Jobbet kommer att visas PÅ detta datum.")

    locked = models.BooleanField(help_text="Om jobbet ska vara låst. "
                                           "Överskrider datumen nedan.")
    locked_after = models.DateField(default=default_locked_after,
                                    help_text="EFTER detta datum kommer jobbet att låsas.")
    locked_until = models.DateField(default=default_locked_until,
                                    help_text="Jobbet kommer att låsas upp PÅ detta datum.")

    slug = models.SlugField(max_length=100, null=True, blank=True)

    types = models.ManyToManyField("Type", blank=True)
    users = models.ManyToManyField("accounts.User", blank=True, related_name="jobs")

    def __str__(self):
        return self.name

    def clean(self):
        if self.hidden_until > self.hidden_after:
            raise ValidationError({
                "hidden_until": "'Hidden until' has to be before 'Hidden after'.",
                "hidden_after": "'Hidden until' has to be before 'Hidden after'.",
            })

        if self.locked_until > self.locked_after:
            raise ValidationError({
                "locked_until": "'Locked until' has to be before 'Locked after'.",
                "locked_after": "'Locked until' has to be before 'Locked after'.",
            })

        if self.start_time > self.end_time:
            raise ValidationError({
                "start_time": "'Start time' has to be before 'End time'.",
                "end_time": "'Start time' has to be before 'End time'.",
            })

    def save(self, *args, **kwargs):
        res = super(Job, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = "-".join([slugify(self.name), str(self.id)])
            self.save()
        return res

    def short_desc(self):
        if len(self.description) > 40:
            return self.description[:40] + "..."
        return self.description

    def short_name(self):
        if len(self.name) > 20:
            return self.name[:20] + "..."
        return self.name

    def url(self):
        return settings.DEFAULT_DOMAIN + \
               reverse("fadderanmalan:jobsignup_detail", args=[self.slug])

    @staticmethod
    def group_by_date(queryset):
        day_grouped = OrderedDict()

        for job in queryset.order_by("date"):
            date = job.date.strftime("%d %b")

            if date not in day_grouped.keys():
                day_grouped[date] = [job]
            else:
                day_grouped[date].append(job)

        return day_grouped

    def full(self):
        return self.users.count() == self.slots

    def full_status(self):
        count = self.users.count()

        if count == 0:
            return "empty"
        if count == self.slots:
            return "full"
        return "partial"

    def locked_status(self):
        return "locked" if self.is_locked() else "unlocked"

    def is_hidden(self):
        today = timezone.now().date()
        return self.hidden or not (self.hidden_until <= today <= self.hidden_after)

    def is_locked(self):
        today = timezone.now().date()
        return self.locked or not (self.locked_until <= today <= self.locked_after)

    @staticmethod
    def is_hidden_query_filter():
        today = timezone.now().date()
        return Q(hidden=True) | ~(Q(hidden_until__lte=today) & Q(hidden_after__gte=today))

    @staticmethod
    def is_locked_query_filter():
        today = timezone.now().date()
        return Q(locked=True) | ~(Q(locked_until__lte=today) & Q(locked_after__gte=today))

    def has_enter_queue(self):
        return self.enter_queue.count() > 0

    def has_leave_queue(self):
        return self.leave_queue.count() > 0

    def dequeue(self):
        dequeued = []
        while not self.full():
            try:
                eq = EnterQueue.get_first(self)
                eq.apply()
                dequeued.append(eq.user)
            except EnterQueue.DoesNotExist:
                break
        return dequeued
