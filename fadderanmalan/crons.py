from uwsgidecorators import cron
from datetime import timedelta
from django.utils import timezone

from fadderjobb.utils import notify_user

from .models import Job


@cron(0, 8, -1, -1, -1)
def notify_jobs_tomorrow():
    tomorrow = (timezone.now() + timedelta(days=1)).date().isoformat()

    jobs = Job.objects.filter(start_date=tomorrow).all()

    user_jobs = {}

    for job in jobs:
        for user in job.users.all():
            if user in user_jobs:
                user_jobs.get(user).append(job.name)
            else:
                user_jobs[user] = [job.name]

    for user, jobs in user_jobs.all():
        notify_user(user, template="job_reminder", template_context=dict(
            user=user,
            jobs=jobs,
        ))
