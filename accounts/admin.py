from django.contrib import admin

from fadderanmalan.admin.admin import JobsInline

from .models import Fadder


class FadderAdmin(admin.ModelAdmin):
    model = Fadder

    inlines = [
        JobsInline,
    ]

admin.site.register(Fadder, FadderAdmin)

