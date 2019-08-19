from uwsgidecorators import cron
from datetime import timedelta
from django.utils import timezone

from fadderjobb.utils import notify_user

from .models import Job


@cron(0, 12, -1, -1, -1)
def notify_jobs_tomorrow(num):
    tomorrow = (timezone.now() + timedelta(days=1)).date().isoformat()

    jobs = Job.objects.filter(start_date=tomorrow).all()

    user_jobs = {}

    for job in jobs:
        for user in job.users.all():
            job_user = job.jobuser_set.get(user=user)
            if user in user_jobs:
                user_jobs.get(user).append((job, job_user))
            else:
                user_jobs[user] = [(job, job_user)]

    for user, vals in user_jobs.items():
        notify_user(user, template="job_reminder", template_context=dict(
            user=user,
            jobs=[v[0] for v in vals],
            leavequeue_jobs=[v[0] for v in vals if v[1].wants_to_leave()],
        ))
