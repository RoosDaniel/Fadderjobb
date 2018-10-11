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

    eq = EnterQueue.objects.filter(fadder=request.user.fadder, job=job).first()
    lq = LeaveQueue.objects.filter(fadder=request.user.fadder, job=job).first()

    return render(request, "jobdetails.html", dict(
        job=job,
        registered_to_job=request.user.is_authenticated and request.user.fadder in job.fadders.all(),
        queued_for_job=request.user.is_authenticated and eq is not None,
        dequeued_for_job=request.user.is_authenticated and lq is not None,
    ))


def topchart(request):
    # Doing it this way means we only have to call .points() once for each fadder
    fadders = Fadder.objects.filter(user__is_staff=False).all()
    points = [f.points() for f in fadders]

    fadders = [f[0] for f in sorted(zip(fadders, points), key=lambda f: f[1], reverse=True)]

    return render(request, "topchart.html", dict(
        fadders=fadders
    ))
