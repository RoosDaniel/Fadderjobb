from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

from .models import Job
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

    return render(request, "jobdetails.html", dict(
        job=job,
        fadder_registered=request.user.is_authenticated and request.user.fadder in job.fadders.all(),
    ))


@login_required(login_url="accounts:login")
def register_for_job(request, job_id):
    if request.method == "POST":
        job = Job.objects.get(id=job_id)

        if job.full():
            return redirect(request.get_full_path(True))

        job.fadders.add(request.user.fadder)

        return redirect("fadderanmalan:jobsignup_detail", job.slug)
    return redirect("fadderanmalan:jobsignup")


@login_required(login_url="/accounts/login")
def deregister_for_job(request, job_id):
    if request.method == "POST":
        job = Job.objects.get(id=job_id)
        job.fadders.remove(request.user.fadder)

        return redirect("fadderanmalan:jobsignup_detail", job.slug)
    return redirect("fadderanmalan:jobsignup")


def topchart(request):
    # Doing it this way means we only have to call .points() once for each fadder
    fadders = Fadder.objects.filter(user__is_staff=False).all()
    points = [f.points() for f in fadders]

    fadders = [f[0] for f in sorted(zip(fadders, points), key=lambda f: f[1], reverse=True)]

    return render(request, "topchart.html", dict(
        fadders=fadders
    ))
