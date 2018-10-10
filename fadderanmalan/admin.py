from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Type, Job
from accounts.models import Fadder


class JobsInline(admin.TabularInline):
    verbose_name = "Fadderjobb"
    verbose_name_plural = "Fadderjobb"

    model = Job.fadders.through


class FadderAdmin(admin.ModelAdmin):
    model = Fadder

    inlines = [
        JobsInline,
    ]


class JobAdmin(admin.ModelAdmin):
    model = Job

    inlines = [
        JobsInline,
    ]

    exclude = [
        "fadders",
    ]


admin.site.register(Type)
admin.site.register(Job, JobAdmin)
admin.site.register(Fadder, FadderAdmin)
