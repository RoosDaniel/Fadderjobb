import re
from datetime import datetime

from django.conf import settings
from django.urls import reverse
from django.http import Http404
from django.utils.timezone import get_current_timezone

from django_ical.views import ICalFeed

from accounts.models import User


class JobFeed(ICalFeed):
    product_id = '-//fadderjobb.staben.info/calendar'
    timezone = str(get_current_timezone())
    file_name = "jobs.ics"

    def __call__(self, request, *args, **kwargs):
        self.request = request

        if "user" not in kwargs:
            raise Http404("Kunde inte hitta användaren.")

        try:
            self.user = User.objects.filter(username=kwargs["user"]).first()
        except User.DoesNotExist:
            raise Http404("Kunde inte hitta användaren '%s'" % kwargs["user"])

        self.file_name = "jobs_{}.ics".format(self.user.username)

        return super(JobFeed, self).__call__(request, *args, **kwargs)

    def items(self):
        return self.user.jobs.all().order_by("-start_date")

    def item_guid(self, item):
        url = re.compile(r"https?://(www\.)?")
        return url.sub("", "{}@{}".format(item.slug, settings.DEFAULT_DOMAIN))

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description

    def item_start_datetime(self, item):
        return datetime.combine(item.start_date, item.start_time)

    def item_end_datetime(self, item):
        return datetime.combine(item.end_date, item.end_time)

    def item_link(self, item):
        return item.url()
