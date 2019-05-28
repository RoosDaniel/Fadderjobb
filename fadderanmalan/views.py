from django.contrib.auth import get_user_model
from django.db.models import Count, F, Q
from django.http import Http404
from django.shortcuts import render, redirect

from .models import Job, Type
from . import utils
from .exceptions import UserError


def job_list(request):
    jobs = Job.objects.order_by("date") \
        .filter(~Job.is_hidden_query_filter()) \
        .all()

    if not request.user.is_superuser:
        # First, remove all jobs that has a viewing requirement
        jobs = jobs.filter(only_visible_to=None)

        # Then add back the ones that are allowed for this user
        if request.user.is_authenticated:
            for group in request.user.groups.all():
                group_jobs = group.jobs.filter(~Job.is_hidden_query_filter())  # Remove hidden jobs
                jobs = jobs.union(group_jobs)

    search = request.GET.get("search", "")

    if search != "":
        jobs = jobs.filter(Q(name__icontains=search.lower()) | Q(description__icontains=search.lower()))

    full = request.GET.get("filter-full", None)

    if full == "1":
        jobs = jobs.annotate(users_count=Count("users")).filter(slots=F("users_count"))
    elif full == "0":
        jobs = jobs.annotate(users_count=Count("users")).exclude(slots=F("users_count"))

    signedup = request.GET.get("filter-signedup", None)

    if signedup == "1":
        jobs = jobs.filter(id__in=request.user.jobs.values_list('id', flat=True))
    elif signedup == "0":
        jobs = jobs.exclude(id__in=request.user.jobs.values_list('id', flat=True))

    leavequeue = request.GET.get("filter-leavequeue", None)

    if leavequeue == "1":
        jobs = jobs.exclude(leave_queue=None)
    elif leavequeue == "0":
        jobs = jobs.filter(leave_queue=None)

    enterqueue = request.GET.get("filter-enterqueue", None)

    if enterqueue == "1":
        jobs = jobs.exclude(enter_queue=None)
    elif enterqueue == "0":
        jobs = jobs.filter(enter_queue=None)

    jobtype = request.GET.get("jobtype", "")

    if jobtype != "":
        jobs = jobs.filter(types__name__iexact=jobtype)

    # Call me paranoid, but I really don't want duplicates
    jobs = jobs.distinct()

    day_grouped = Job.group_by_date(jobs)

    return render(request, "fadderanmalan/job_list.html", dict(
        day_grouped=day_grouped,
        jobtypes=(t.name for t in Type.objects.all()),
        filter_search=search,
        filter_signedup=signedup,
        filter_full=full,
        filter_leavequeue=leavequeue,
        filter_enterqueue=enterqueue,
        filter_jobtype=jobtype
    ))


def job_details(request, slug):
    try:
        job = Job.objects.get(slug=slug, hidden=False)

        if job.only_visible_to.all():
            if request.user.is_anonymous:
                raise Job.DoesNotExist

            if not request.user.is_superuser:
                # Get the intersection of allowed groups and the user's groups
                common_groups = set(job.only_visible_to.all()) & set(request.user.groups.all())

                # If there are no groups, raise 404
                if not common_groups:
                    raise Job.DoesNotExist
    except Job.DoesNotExist:
        raise Http404("Kunde inte hitta jobbet '%s'" % slug)

    if request.method == "POST" and request.user.can_register():
        try:
            utils.handle_register(request, job)
        except UserError as e:
            return render(request, "400.html", dict(exception=str(e)))

    hint_text, button_text, button_name = utils.generate_registration_text(request, job)

    return render(request, "fadderanmalan/job_details.html", dict(
        job=job,
        hint_text=hint_text,
        button_text=button_text,
        button_name=button_name
    ))
