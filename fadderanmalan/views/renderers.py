from django.shortcuts import render

from fadderanmalan.models import Job, EnterQueue, LeaveQueue
from accounts.models import Fadder


def index(request):
    return render(request, "index.html")


def jobsignup(request):
    jobs = Job.objects.order_by("date").all()

    search = request.GET.get("search", "")

    if search != "":
        jobs = jobs.filter(name__contains=search)

    day_grouped = Job.group_by_date(jobs)

    return render(request, "jobsignup.html", dict(
        prev_search=search,
        day_grouped=day_grouped,
    ))


def jobdetails(request, slug):
    job = Job.objects.get(slug=slug)

    if request.user.is_authenticated:
        registered_to_job = request.user.fadder in job.fadders.all()
        queued_enter_job = job.enter_queue.filter(fadder=request.user.fadder).first()
        queued_leave_job = job.leave_queue.filter(fadder=request.user.fadder).first()
    else:
        registered_to_job = False
        queued_enter_job = False
        queued_leave_job = False

    return render(request, "jobdetails.html", dict(
        job=job,
        registered_to_job=registered_to_job,
        queued_enter_job=queued_enter_job,
        queued_leave_job=queued_leave_job,
        has_enter_queue=job.enter_queue.count() > 0,
        has_leave_queue=job.leave_queue.count() > 0,
    ))


def topchart(request):
    # Doing it this way means we only have to call .points() once for each fadder
    fadders = Fadder.objects.filter(user__is_staff=False).all()
    points = [f.points() for f in fadders]

    fadders = [f[0] for f in sorted(zip(fadders, points), key=lambda f: f[1], reverse=True)]

    return render(request, "topchart.html", dict(
        fadders=fadders
    ))
