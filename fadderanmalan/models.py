from collections import OrderedDict

from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.urls import reverse

from fadderjobb.staben_mail import send_mail


class Type(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


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

        job_url = "https://fadderjobb.staben.info" + \
                  reverse("fadderanmalan:jobsignup_detail", args=[self.job.slug])

        send_mail(self.user.email, "Du har fått en plats på ett jobb du har köat för",
                  "Du har fått en plats på jobbet '%s'. Se jobbet här: %s" % (self.job.name, job_url))


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

        job_url = "https://fadderjobb.staben.info" + \
                  reverse("fadderanmalan:jobsignup_detail", args=[self.job.slug])

        send_mail(self.user.email, "Någon har tagit en plats på ett jobb du vill lämna",
                  "Någon har tagit din plats på jobbet '%s'. Se jobbet här: %s" % (self.job.name, job_url))


class Job(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField(null=True, blank=True)
    duration = models.IntegerField()
    points = models.IntegerField()
    slots = models.IntegerField()

    locked = models.BooleanField()

    slug = models.SlugField(max_length=100, null=True, blank=True)

    types = models.ManyToManyField("Type", blank=True)
    users = models.ManyToManyField("accounts.User", blank=True, related_name="jobs")

    def __str__(self):
        return self.name

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
        return "locked" if self.locked else "unlocked"

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
