def set_locked(modeladmin, request, queryset):
    queryset.update(locked=True)
set_locked.short_description = "Lock selected jobs"
