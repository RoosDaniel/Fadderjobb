def job_set_locked(modeladmin, request, queryset):
    queryset.update(locked=True)
job_set_locked.short_description = "Lock selected jobs"


def job_set_hidden(modeladmin, request, queryset):
    queryset.update(hidden=True)
job_set_hidden.short_description = "Hide selected jobs"
