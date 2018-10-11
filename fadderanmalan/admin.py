from django.contrib import admin

from .models import Type, EnterQueue, LeaveQueue, Job


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


admin.site.register(Type)
admin.site.register(EnterQueue)
admin.site.register(LeaveQueue)

admin.site.register(Job, JobAdmin)
