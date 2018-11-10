from django.contrib import admin

from fadderanmalan.models import Type, EnterQueue, LeaveQueue, Job
from .actions import set_locked


class JobsInline(admin.TabularInline):
    verbose_name = "Fadderjobb"
    verbose_name_plural = "Fadderjobb"

    model = Job.fadders.through


class JobAdmin(admin.ModelAdmin):
    model = Job

    inlines = [
        JobsInline,
    ]

    exclude = [
        "fadders",
    ]

    actions = [set_locked]

    list_filter = ["locked", "types", ("date", admin.AllValuesFieldListFilter)]

    search_fields = ["name"]


class EnterQueueAdmin(admin.ModelAdmin):
    model = EnterQueue

    search_fields = ["job__name", "fadder__user__username"]


class LeaveQueueAdmin(admin.ModelAdmin):
    model = LeaveQueue

    search_fields = ["job__name", "fadder__user__username"]


admin.site.register(Type)
admin.site.register(EnterQueue, EnterQueueAdmin)
admin.site.register(LeaveQueue, LeaveQueueAdmin)

admin.site.register(Job, JobAdmin)
