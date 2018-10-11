from django.shortcuts import render, redirect
from django.contrib.auth import login as django_login, logout as django_logout

from .forms import FadderCreationForm, FadderLoginForm
from .models import Fadder
from fadderanmalan.models import Job


def profile(request, liu_id):
    fadder = Fadder.objects.get(user__username=liu_id)
    day_grouped = Job.group_by_date(fadder.jobs.all())

    return render(request, "accounts/profile.html", dict(
        fadder=fadder,
        day_grouped=day_grouped
    ))


def my_profile(request):
    return redirect("accounts:profile", request.user.username)

    # day_grouped = Job.group_by_date(request.user.fadder.jobs.all())

    # return render(request, "accounts/my_profile.html", dict(
    #     day_grouped=day_grouped
    # ))


def login(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        form = FadderLoginForm(data=request.POST)
        if form.is_valid():
            django_login(request, form.get_user())
            return redirect("accounts:my_profile")
    else:
        form = FadderLoginForm()

    return render(request, "accounts/login.html", dict(
        form=form
    ))


def logout(request):
    if request.method == "POST":
        django_logout(request)
        return redirect("/")


def registration(request):
    if request.user.is_authenticated:
        return redirect("accounts:my_profile")

    if request.method == "POST":
        form = FadderCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email = form.cleaned_data["email"]
            user.save()

            fadder = Fadder(user=user)
            fadder.save()

            django_login(request, user)

            return redirect("accounts:my_profile")
    else:
        form = FadderCreationForm()

    return render(request, "accounts/registration.html", dict(
        form=form
    ))
