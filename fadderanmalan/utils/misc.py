from typing import List

from django.contrib.auth import get_user_model

from ..models import Job


User = get_user_model()


# Removes all jobs that the user cannot view due to insufficient permissions
def filter_jobs_for_user(user: User, jobs: List[Job]) -> List[Job]:
    original_jobs = jobs[:]

    if not user.is_superuser:
        # First, remove all jobs that has a viewing requirement
        jobs = jobs.filter(only_visible_to=None)

        # Then add back the ones that are allowed for this user
        if user.is_authenticated:
            for group in user.groups.all():
                group_jobs = group.jobs.filter(~Job.is_hidden_query_filter())  # Remove hidden jobs
                group_jobs = group_jobs.filter(id__in=[job.pk for job in original_jobs])
                jobs = jobs.union(group_jobs)

    return jobs
