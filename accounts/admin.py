from django.contrib import admin
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import models

from loginas.utils import login_as

from fadderanmalan.models import EquipmentOwnership
from fadderjobb.filters import DropdownFilterRelated


User = get_user_model()


class JobsInline(admin.TabularInline):
    verbose_name = "Job"
    verbose_name_plural = "Jobs"

    model = User.jobs.through

    fields = ("job",)

    extra = 0


class EquipmentOwnershipInline(admin.TabularInline):
    verbose_name = "Dispensed Equipment"
    verbose_name_plural = "Dispensed Equipment"

    model = EquipmentOwnership

    extra = 0

    readonly_fields = ("dispensed_at",)

    show_change_link = True


class UserAdmin(admin.ModelAdmin):
    model = User

    exclude = ("password", "first_name", "last_name", "is_active")

    fields = (
        "username",
        "name",
        "email",
        "phone_number",
        "motto",
        "read_guide",
        "is_superuser",
        "is_staff",
        "groups",
        "user_permissions",
        "date_joined",
        "last_login",
    )

    readonly_fields = ("date_joined", "last_login")

    inlines = (
        JobsInline,
        EquipmentOwnershipInline,
    )

    list_display = ("username", "name", "points", "equipment")

    list_filter = (("jobs", DropdownFilterRelated), ("equipments__equipment", DropdownFilterRelated))

    def equipment(self, obj):
        return ", ".join(str(eq.equipment) for eq in obj.equipments.all())

    def response_change(self, request, obj):
        if "_loginas" in request.POST:
            login_as(obj, request)

            return HttpResponseRedirect(reverse("index"))
        return super().response_change(request, obj)

    def get_queryset(self, request):
        qs = super(UserAdmin, self).get_queryset(request)
        qs = qs.annotate(models.Sum('jobs__points'))
        return qs

    def points(self, obj):
        return obj.jobs__points__sum or 0

    points.admin_order_field = 'jobs__points'

admin.site.register(User, UserAdmin)
