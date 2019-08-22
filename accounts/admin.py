from django.contrib import admin
from django.contrib.auth import get_user_model
from django.apps import apps
from django.contrib.admin.filters import BooleanFieldListFilter
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.utils.html import format_html
from django.urls import reverse
from django.db import models

from loginas.utils import login_as

from fadderanmalan.models import EquipmentOwnership, EnterQueue
from fadderjobb.filters import DropdownFilterRelated


User = get_user_model()


class JobsInline(admin.TabularInline):
    verbose_name = "Job"
    verbose_name_plural = "Jobs"

    model = User.jobs.through

    fields = ("job",)

    autocomplete_fields = ("job",)

    extra = 0


class EQInline(admin.TabularInline):
    verbose_name = "Enterqueue"
    verbose_name_plural = "EnterQueue"

    model = EnterQueue

    autocomplete_fields = ("job",)

    extra = 0


class EquipmentOwnershipInline(admin.TabularInline):
    verbose_name = "Dispensed Equipment"
    verbose_name_plural = "Dispensed Equipment"

    model = EquipmentOwnership

    extra = 0

    readonly_fields = ("dispensed_at",)

    autocomplete_fields = ("job", "equipment")

    show_change_link = True


class UserAdmin(admin.ModelAdmin):
    model = User

    exclude = ("password", "first_name", "last_name", "is_active")

    fields = (
        "url",
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

    readonly_fields = ("date_joined", "last_login", "url")

    inlines = (
        JobsInline,
        EquipmentOwnershipInline,
        EQInline,
    )

    list_display = ("username", "name", "points", "equipment")

    search_fields = ("username", "name")

    list_filter = [
        ("is_superuser", BooleanFieldListFilter),
        ("jobs", DropdownFilterRelated),
        ("equipments__equipment", DropdownFilterRelated),
        ("groups", DropdownFilterRelated),
    ]

    def get_ordering(self, request):
        return ['username']

    def url(self, obj):
        url = obj.url()

        if not url:
            return ""
        return format_html("<a href='{url}'>{url}</a>", url=obj.url())
    url.short_description = "URL"

    def equipment(self, obj):
        return ", ".join(str(eq.equipment) for eq in obj.equipments.all())

    def response_change(self, request, obj):
        if "_loginas" in request.POST:
            if not request.user.is_superuser:
                return HttpResponseForbidden()
            login_as(obj, request)

            return HttpResponseRedirect(reverse("index"))
        return super().response_change(request, obj)


admin.site.register(User, UserAdmin)
