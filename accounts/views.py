from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as django_login, logout as django_logout, get_user_model
from django.contrib.auth.decorators import login_required

from .forms import FadderEditForm, FadderCreationForm, FadderLoginForm
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


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = FadderEditForm(request.user, data=request.POST)

        if form.is_valid():
            request.user.email = form.cleaned_data.get("email", request.user.email)
            request.user.motto = form.cleaned_data.get("motto", request.user.motto)

            if form.cleaned_data.get("password1"):
                request.user.set_password(form.cleaned_data.get("password1"))
                request.user.save()

                messages.add_message(request, messages.INFO,
                                     "Du har bytt ditt lösenord, logga in igen.")

                # TODO Logout all sessions

                django_logout(request)

                return redirect("accounts:login")

            request.user.save()

            messages.add_message(request, messages.INFO,
                                 "Din profil har uppdaterats. <a href='/accounts/my_profile'>Se dina ändringar.</a>")
        else:
            messages.add_message(request, messages.ERROR,
                                 "Ett eller flera problem uppstod.")
    else:
        form = FadderEditForm(request.user, initial={
            "email": request.user.email,
            "motto": request.user.motto
        })

    return render(request, "accounts/edit_profile.html", dict(
        form=form
    ))


# Unused
def login(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        form = FadderLoginForm(data=request.POST)
        if form.is_valid():
            django_login(request, form.get_user())
            return redirect(request.POST.get("next") or "accounts:my_profile")
    else:
        form = FadderLoginForm()

    return render(request, "accounts/login.html", dict(
        form=form
    ))


# Unused
def logout(request):
    if request.method == "POST":
        django_logout(request)
    return redirect("/")


# Unused
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
