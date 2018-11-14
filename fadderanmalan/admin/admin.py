from django.contrib import admin

from fadderanmalan.models import Type, EnterQueue, LeaveQueue, Job
from .actions import set_locked


class JobsInline(admin.TabularInline):
    verbose_name = "Fadderjobb"
    verbose_name_plural = "Fadderjobb"

    model = Job.users.through


class JobAdmin(admin.ModelAdmin):
    model = Job

    inlines = [
        JobsInline,
    ]

    list_display = ["name", "date", "locked", "signed_up"]

    exclude = [
        "fadders",
    ]

    actions = [set_locked]

    list_filter = ["locked", "types", ("date", admin.AllValuesFieldListFilter)]

    search_fields = ["name"]

    def signed_up(self, obj):
        return ", ".join([user.username for user in obj.users.all()])


class EnterQueueAdmin(admin.ModelAdmin):
    model = EnterQueue

    list_display = ["job", "user"]

    search_fields = ["job__name", "user__username"]


class LeaveQueueAdmin(admin.ModelAdmin):
    model = LeaveQueue

    list_display = ["job", "user"]

    search_fields = ["job__name", "user__username"]


admin.site.register(Type)
admin.site.register(EnterQueue, EnterQueueAdmin)
admin.site.register(LeaveQueue, LeaveQueueAdmin)

admin.site.register(Job, JobAdmin)
