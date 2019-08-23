from django.db.models import Q
from django.contrib.auth import get_user_model

from ..models import Job


User = get_user_model()


# Removes all jobs that the user cannot view due to insufficient permissions
def filter_jobs_for_user(user: User, jobs):
    if not user.is_superuser:
        jobs = jobs.filter(Q(only_visible_to__in=user.groups.all()) | Q(only_visible_to__isnull=True))

    return jobs
