from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.db.models import Q, Count

from django.contrib.admin.filters import BooleanFieldListFilter

from fadderanmalan.models import Type, EnterQueue, LeaveQueue, Job, Equipment, EquipmentOwnership, ActionLog
from .actions import job_set_locked, job_set_hidden
from .forms import JobAdminForm

from fadderjobb.filters import DropdownFilterRelated, DropdownFilter


class UsersInline(admin.TabularInline):
    verbose_name = "Registered user"
    verbose_name_plural = "Registered users"

    model = Job.users.through

    extra = 0

    fields = ("user",)


class LQInline(admin.TabularInline):
    verbose_name = "Leavequeue"
    verbose_name_plural = "Leavequeue"

    model = LeaveQueue

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        field = super(LQInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name == "user":
            if request.obj_ is not None:
                field.queryset = field.queryset.filter(id__in=request.obj_.users.all())
            else:
                field.queryset = field.queryset.none()

        return field


class EQInline(admin.TabularInline):
    verbose_name = "Enterqueue"
    verbose_name_plural = "EnterQueue"

    model = EnterQueue

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        field = super(EQInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name == "user":
            if request.obj_ is not None:
                field.queryset = field.queryset.filter(~Q(id__in=request.obj_.users.all()))
            else:
                field.queryset = field.queryset.none()

        return field


class JobAdmin(admin.ModelAdmin):
    model = Job
    form = JobAdminForm

    inlines = (
        UsersInline,
        LQInline,
        EQInline
    )

    list_display = ("name", "start_date", "locked", "hidden", "slots_taken")

    exclude = ("users", "slug")

    actions = (job_set_locked, job_set_hidden)

    list_filter = ("locked", "hidden", "types", ("start_date", DropdownFilter), "only_visible_to")

    search_fields = ("name",)

    def registered(self, obj):
        return ", ".join([user.username for user in obj.users.all()])

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context.update({'help_text': 'Sökbara fält: jobb-namn.'})

        return super(JobAdmin, self)\
            .changelist_view(request, extra_context=extra_context)

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

    def get_form(self, request, obj=None, **kwargs):
        request.obj_ = obj

        return super(JobAdmin, self).get_form(request, obj, **kwargs)

    def get_queryset(self, request):
        qs = super(JobAdmin, self).get_queryset(request)
        qs = qs.annotate(user_count=Count('users'))
        return qs

    def slots_taken(self, obj: Job):
        return "%s/%s" % (obj.user_count, obj.slots)

    slots_taken.admin_order_field = "user_count"


class EnterQueueAdmin(admin.ModelAdmin):
    model = EnterQueue

    list_display = ("job", "user")

    search_fields = ("user__username", "job__name")

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context.update({'help_text': 'Sökbara fält: liu-id, jobb-namn.'})

        return super(EnterQueueAdmin, self)\
            .changelist_view(request, extra_context=extra_context)


class LeaveQueueAdmin(admin.ModelAdmin):
    model = LeaveQueue

    list_display = ("job", "user")

    search_fields = ("user__username", "job__name")

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context.update({'help_text': 'Sökbara fält: liu-id, jobb-namn.'})

        return super(LeaveQueueAdmin, self)\
            .changelist_view(request, extra_context=extra_context)


class EquipmentAdmin(admin.ModelAdmin):
    model = Equipment

    list_display = ("name", "size")

    def render_change_form(self, request, context, *args, **kwargs):
        context.update({'help_text': 'Generella utrustningar. Skapa dessa innan utdelning.'})

        return super(EquipmentAdmin, self)\
            .render_change_form(request, context, *args, **kwargs)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context.update({'help_text': 'Generella utrustningar. Skapa dessa innan utdelning.'})

        return super(EquipmentAdmin, self)\
            .changelist_view(request, extra_context=extra_context)


class EquipmentOwnershipAdmin(admin.ModelAdmin):
    model = EquipmentOwnership

    list_display = ("name", "size", "fadder", "job")

    search_fields = ("fadder__username", "job__name")

    list_filter = (("equipment", DropdownFilterRelated),)

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

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context.update({'help_text': 'Sökbara fält: liu-id, jobb-namn.'})

        return super(EquipmentOwnershipAdmin, self)\
            .changelist_view(request, extra_context=extra_context)

    def name(self, obj):
        return obj.equipment.name

    def size(self, obj):
        return obj.equipment.size


class ActionLogAdmin(admin.ModelAdmin):
    model = ActionLog

    list_display = ("user", "job", "created", "action_type")

    list_filter = (("type", DropdownFilter),)

    search_fields = ("user__username", "job__name", "user__name")

    def action_type(self, obj: ActionLog):
        return obj.type


admin.site.register(Type)
admin.site.register(EnterQueue, EnterQueueAdmin)
admin.site.register(LeaveQueue, LeaveQueueAdmin)

admin.site.register(Job, JobAdmin)

admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(EquipmentOwnership, EquipmentOwnershipAdmin)

admin.site.register(ActionLog, ActionLogAdmin)
