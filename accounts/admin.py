from django.contrib import admin
from django.contrib.auth import get_user_model

from fadderanmalan.models import EquipmentOwnership
from fadderjobb.filters import DropdownFilterRelated


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

    # fields = ("username", )

    list_display = ("username", "equipment")

    list_filter = (("jobs", DropdownFilterRelated), ("equipments__equipment", DropdownFilterRelated))

    def equipment(self, obj):
        return ", ".join(str(eq.equipment) for eq in obj.equipments.all())

admin.site.register(User, UserAdmin)
