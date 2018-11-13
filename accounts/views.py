from django.shortcuts import render, redirect
from django.contrib.auth import login as django_login, logout as django_logout, get_user_model

from .forms import FadderCreationForm, FadderLoginForm
from fadderanmalan.models import Job


User = get_user_model()


def profile(request, liu_id):
    user = User.objects.get(username=liu_id)
    day_grouped = Job.group_by_date(user.jobs.all())

    return render(request, "accounts/profile.html", dict(
        user=user,
        day_grouped=day_grouped
    ))


def my_profile(request):
    return redirect("accounts:profile", request.user.username)

    # day_grouped = Job.group_by_date(request.user.jobs.all())

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

            django_login(request, user)

            return redirect("accounts:my_profile")
    else:
        form = FadderCreationForm()

    return render(request, "accounts/registration.html", dict(
        form=form
    ))
