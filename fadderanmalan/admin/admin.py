from django.contrib import admin, messages
from django.http import HttpResponseRedirect

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
        "users",
    ]

    actions = [set_locked]

    list_filter = ["locked", "types", ("date", admin.AllValuesFieldListFilter)]

    search_fields = ["name"]

    change_form_template = "admin/fadderanmalan/change_job.html"

    def signed_up(self, obj):
        return ", ".join([user.username for user in obj.users.all()])

    def response_change(self, request, obj):
        if "_dequeue" in request.POST:
            if obj.full():
                messages.add_message(request, messages.ERROR, "Job is full.")
            else:
                added = []

                while not obj.full():
                    try:
                        eq = EnterQueue.get_first(job=obj)
                        obj.users.add(eq.user)
                        eq.delete()
                        obj.save()
                        added.append(eq.user.username)
                    except EnterQueue.DoesNotExist:
                        break

                if len(added) > 0:
                    messages.add_message(request, messages.INFO, "Users '%s' dequeued." % "', '".join(added))
                else:
                    messages.add_message(request, messages.ERROR, "No users to dequeue.")

            return HttpResponseRedirect(".")
        return super().response_change(request, obj)


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
