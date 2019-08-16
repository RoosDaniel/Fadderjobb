from django.shortcuts import render
from django.http import HttpResponseRedirect

from .utils import notify_registered


def job_set_locked(modeladmin, request, queryset):
    queryset.update(locked=True)

job_set_locked.short_description = "Lock selected jobs"


def job_set_hidden(modeladmin, request, queryset):
    queryset.update(hidden=True)

job_set_hidden.short_description = "Hide selected jobs"


def job_notify_registered(modeladmin, request, queryset):
    if "apply" in request.POST:
        notify_registered(request, queryset.all(), request.POST.get("content"))

        return HttpResponseRedirect(request.get_full_path())

    return render(request, "admin/fadderanmalan/job/notify_registered_action.html", dict(
        jobs=queryset.all(), title="Send notification"))

job_notify_registered.short_description = "Notify registered users"
