from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as django_login, logout as django_logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import Http404

from loginas.views import user_logout as la_restore

from .forms import FadderEditForm
from fadderanmalan.models import Job

from trade.models import Trade

User = get_user_model()


def profile(request, username):
    if username == request.user.username:
        return render(request, "accounts/my_profile.html", dict(
            non_returned_equipment_ownerships=request.user.equipments.all(),
            day_grouped=Job.group_by_date(request.user.jobs.all()),
        ))

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("Kunde inte hitta användaren '%s'" % username)
    day_grouped = Job.group_by_date(user.jobs.all())

    if request.user.is_anonymous:
        trade = None
    else:
        try:
            trade = Trade.get_trade(request.user, user)
        except Trade.DoesNotExist:
            trade = None

    return render(request, "accounts/profile.html", dict(
        user=user,
        day_grouped=day_grouped,
        trade=trade,
    ))


def my_profile(request):
    return redirect("accounts:profile", request.user.username)


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = FadderEditForm(data=request.POST)

        if form.is_valid():
            request.user.email = form.cleaned_data.get("email")

            # The "or None" part is necessary since the form will submit with empty strings, which means we
            # can't do checks like "if phone is None" (done in for example warn_no_phone_number middleware)
            request.user.phone_number = form.cleaned_data.get("phone_number") or None
            request.user.motto = form.cleaned_data.get("motto")
            request.user.name = form.cleaned_data.get("name")

            request.user.save()

            messages.add_message(request, messages.INFO,
                                 "Din profil har uppdaterats. "
                                 "<a href='%s'>Se dina ändringar.</a>" % reverse("accounts:my_profile"))
        else:
            messages.add_message(request, messages.ERROR,
                                 "Ett eller flera problem uppstod.")
    else:
        form = FadderEditForm(initial=dict(
            email=request.user.email,
            phone_number=request.user.phone_number,
            motto=request.user.motto,
        ))

    return render(request, "accounts/edit_profile.html", dict(
        form=form,
    ))


@login_required
def restore_impersonation(request):
    # Clear any messages generated by the impersonated login before switching back
    list(messages.get_messages(request))

    return la_restore(request)
