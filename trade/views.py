from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, Http404

from .forms import TradeForm
from .models import Trade


User = get_user_model()


@login_required
def start(request, receiver_username):
    try:
        receiver = User.objects.get(username=receiver_username)
    except User.DoesNotExist:
        raise Http404("Kunde inte hitta användaren '%s'" % receiver_username)

    try:
        Trade.objects.get(sender=request.user, receiver=receiver)

        return render(request, "400.html", dict(
            exception="Du har redan skickat ett bytesförslag till den här personen."
        ))
    except Trade.DoesNotExist:
        pass

    try:
        Trade.objects.get(sender=receiver, receiver=request.user)

        return render(request, "400.html", dict(
            exception="Den här användaren har redan skickat en bytesförfrågan till dig. "
                      "Svara på den innan du skickar en ny förfrågan."
        ))
    except Trade.DoesNotExist:
        pass

    if request.method == "POST":
        form = TradeForm(sender=request.user, receiver=receiver, data=request.POST)

        if form.is_valid():
            trade = form.save(commit=False)

            trade.sender = request.user
            trade.receiver = receiver

            trade.save()
            trade.notify_receiver()

            messages.add_message(request, messages.INFO,
                                 "Bytesförfrågan har skickats på mail till %s." % receiver.username)
        else:
            messages.add_message(request, messages.ERROR,
                                 "Ett eller flera problem uppstod.")
    else:
        form = TradeForm(sender=request.user, receiver=receiver)

    return render(request, "trade/start.html", dict(
        trade_form=form,
        receiver=receiver,
    ))


@login_required
def complete(request, sender_username):
    try:
        sender = User.objects.get(username=sender_username)
    except User.DoesNotExist:
        raise Http404("Kunde inte hitta användaren '%s'" % sender_username)

    try:
        Trade.objects.get(sender=sender, receiver=request.user)
    except Trade.DoesNotExist:
        raise Http404("Bytesförfrågan hittades ej. Sändaren kan ha avbrutit förfrågan.")

    if request.method == "POST":
        pass
    else:
        pass
