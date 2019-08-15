from django.contrib import messages

from fadderjobb.utils import notify_user


def notify_registered(request, jobs, message):
    user_jobs = {}

    for job in jobs:
        for user in job.users.all():
            if user in user_jobs:
                user_jobs.get(user).append(job.name)
            else:
                user_jobs[user] = [job.name]

    for user, registered_jobs in user_jobs.items():
        notify_user(user, template="job_notification", template_context=dict(
            jobs=registered_jobs,
            user=user,
            admin=request.user,
            message=message,
        ))

    job_names = ", ".join([job.name for job in jobs])
    messages.add_message(request, messages.INFO, "Notified users registered to jobs %s." % job_names)
