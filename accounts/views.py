from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as django_login, logout as django_logout, get_user_model
from django.contrib.auth.decorators import login_required

from .forms import FadderEditForm
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
        form = FadderEditForm(data=request.POST)

        if form.is_valid():
            request.user.motto = form.cleaned_data.get("motto", request.user.motto)

            request.user.save()

            messages.add_message(request, messages.INFO,
                                 "Din profil har uppdaterats. <a href='/accounts/my_profile'>Se dina ändringar.</a>")
        else:
            messages.add_message(request, messages.ERROR,
                                 "Ett eller flera problem uppstod.")
    else:
        form = FadderEditForm(initial={
            "motto": request.user.motto
        })

    return render(request, "accounts/edit_profile.html", dict(
        form=form
    ))
