from django.contrib import admin, messages
from django.http import HttpResponseRedirect

from fadderanmalan.models import Type, EnterQueue, LeaveQueue, Job, Equipment, EquipmentOwnership
from .actions import job_set_locked, job_set_hidden, equipmentownership_set_returned


class JobsInline(admin.TabularInline):
    verbose_name = "User"
    verbose_name_plural = "Users"

    model = Job.users.through


class LQInline(admin.TabularInline):
    verbose_name = "Leavequeue"
    verbose_name_plural = "Leavequeue"

    model = LeaveQueue


class EQInline(admin.TabularInline):
    verbose_name = "Enterqueue"
    verbose_name_plural = "EnterQueue"

    model = EnterQueue


class JobAdmin(admin.ModelAdmin):
    model = Job

    inlines = (
        JobsInline,
        LQInline,
        EQInline
    )

    list_display = ("name", "date", "locked", "signed_up")

    exclude = ("users",)

    actions = (job_set_locked, job_set_hidden)

    list_filter = ("locked", "types", ("date", admin.AllValuesFieldListFilter))

    search_fields = ("name",)

    change_form_template = "admin/fadderanmalan/change_job.html"

    def signed_up(self, obj):
        return ", ".join([user.username for user in obj.users.all()])

    def response_change(self, request, obj):
        if "_dequeue" in request.POST:
            if obj.full():
                messages.add_message(request, messages.ERROR, "Job is full.")
            else:
                added = obj.dequeue()
                added = [user.username for user in added]

                if len(added) > 0:
                    messages.add_message(request, messages.INFO, "Users '%s' dequeued." % "', '".join(added))
                else:
                    messages.add_message(request, messages.ERROR, "No users to dequeue.")

            return HttpResponseRedirect(".")
        return super().response_change(request, obj)


class EnterQueueAdmin(admin.ModelAdmin):
    model = EnterQueue

    list_display = ("job", "user")

    search_fields = ("job__name", "user__username")


class LeaveQueueAdmin(admin.ModelAdmin):
    model = LeaveQueue

    list_display = ("job", "user")

    search_fields = ("job__name", "user__username")


class EquipmentAdmin(admin.ModelAdmin):
    model = Equipment

    list_display = ("name", "size")


class EquipmentOwnershipAdmin(admin.ModelAdmin):
    model = EquipmentOwnership

    list_display = ("name", "size", "fadder", "job", "returned")

    actions = (equipmentownership_set_returned,)

    search_fields = ("fadder__username", "job__name")

    list_filter = ("equipment", "returned")

    def get_changeform_initial_data(self, request):
        try:
            last = EquipmentOwnership.objects.latest("dispensed_at")

            return {"job": last.job}
        except EquipmentOwnership.DoesNotExist:
            return {}

    def render_change_form(self, request, context, *args, **kwargs):
        context.update({'help_text': ''})
        return super(EquipmentOwnershipAdmin, self)\
            .render_change_form(request, context, *args, **kwargs)


admin.site.register(Type)
admin.site.register(EnterQueue, EnterQueueAdmin)
admin.site.register(LeaveQueue, LeaveQueueAdmin)

admin.site.register(Job, JobAdmin)

admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(EquipmentOwnership, EquipmentOwnershipAdmin)
