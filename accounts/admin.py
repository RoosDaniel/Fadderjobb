from django.contrib import admin
from django.contrib.auth import get_user_model

from fadderanmalan.admin.admin import JobsInline


User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    model = User

    exclude = ("password",)

    inlines = [
        JobsInline,
    ]

admin.site.register(User, UserAdmin)
