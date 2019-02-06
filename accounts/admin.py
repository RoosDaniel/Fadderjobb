from django.contrib import admin
from django.contrib.auth import get_user_model

from fadderanmalan.models import EquipmentOwnership


User = get_user_model()


class JobsInline(admin.TabularInline):
    verbose_name = "Job"
    verbose_name_plural = "Jobs"

    model = User.jobs.through

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

    exclude = ("password",)

    inlines = (
        JobsInline,
        EquipmentOwnershipInline,
    )

    list_filter = ("jobs",)

admin.site.register(User, UserAdmin)
