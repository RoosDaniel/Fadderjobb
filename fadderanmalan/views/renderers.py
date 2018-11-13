from django.shortcuts import render
from django.db.models import Count, F, Q
from django.contrib.auth import get_user_model

from fadderanmalan.models import Job, EnterQueue, LeaveQueue, Type


User = get_user_model()


def index(request):
    return render(request, "index.html")


def jobsignup(request):
    jobs = Job.objects.order_by("date").all()

    search = request.GET.get("search", "")

    if search != "":
        jobs = jobs.filter(Q(name__icontains=search.lower()) | Q(description__icontains=search.lower()))

    full = request.GET.get("full", None)

    if full == "1":
        jobs = jobs.annotate(users_count=Count("users")).filter(slots=F("users_count"))
    elif full == "0":
        jobs = jobs.annotate(users_count=Count("users")).exclude(slots=F("users_count"))

    signedup = request.GET.get("signedup", None)

    if signedup == "1":
        jobs = jobs.filter(users__user__username__contains=request.user.username)
    elif signedup == "0":
        jobs = jobs.exclude(users__user__username__contains=request.user.username)

    leavequeue = request.GET.get("leavequeue", None)

    if leavequeue == "1":
        jobs = jobs.exclude(leave_queue=None)
    elif leavequeue == "0":
        jobs = jobs.filter(leave_queue=None)

    enterqueue = request.GET.get("enterqueue", None)

    if enterqueue == "1":
        jobs = jobs.exclude(enter_queue=None)
    elif enterqueue == "0":
        jobs = jobs.filter(enter_queue=None)

    jobtype = request.GET.get("jobtype", "")

    if jobtype != "":
        jobs = jobs.filter(types__name__iexact=jobtype)

    day_grouped = Job.group_by_date(jobs)

    return render(request, "jobsignup.html", dict(
        day_grouped=day_grouped,
        jobtypes=(t.name for t in Type.objects.all()),
        filter_search=search,
        filter_signedup=signedup,
        filter_full=full,
        filter_leavequeue=leavequeue,
        filter_enterqueue=enterqueue,
        filter_jobtype=jobtype
    ))


def jobdetails(request, slug):
    job = Job.objects.get(slug=slug)

    if request.user.is_authenticated:
        registered_to_job = request.user in job.users.all()
        queued_enter_job = job.enter_queue.filter(user=request.user).first()
        queued_leave_job = job.leave_queue.filter(user=request.user).first()
    else:
        registered_to_job = False
        queued_enter_job = False
        queued_leave_job = False

    return render(request, "jobdetails.html", dict(
        job=job,
        registered_to_job=registered_to_job,
        queued_enter_job=queued_enter_job,
        queued_leave_job=queued_leave_job,
    ))


def topchart(request):
    # Doing it this way means we only have to call .points() once for each user
    users = User.objects.filter(is_staff=False).all()
    points = [f.points() for f in users]

    users = [f[0] for f in sorted(zip(users, points), key=lambda f: f[1], reverse=True)]

    return render(request, "topchart.html", dict(
        users=users
    ))
