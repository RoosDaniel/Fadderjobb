from collections import OrderedDict

from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from accounts.models import Fadder


class Type(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Job(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField(null=True, blank=True)
    duration = models.IntegerField()
    points = models.IntegerField()
    slots = models.IntegerField()

    slug = models.SlugField(max_length=100, null=True, blank=True)

    types = models.ManyToManyField("Type", blank=True)
    fadders = models.ManyToManyField("accounts.Fadder", blank=True, related_name="jobs")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Job, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = "-".join([slugify(self.name), str(self.id)])
            self.save()

    def short_desc(self):
        if len(self.description) > 40:
            return self.description[:40] + "..."
        return self.description

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
        return self.fadders.count() == self.slots

    def full_status(self):
        count = self.fadders.count()

        if count == 0:
            return "empty"
        if count == self.slots:
            return "full"
        return "partial"
