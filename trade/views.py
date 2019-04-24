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
        Trade.get_active(sender=request.user, receiver=receiver)

        return render(request, "400.html", dict(
            exception="Du har redan skickat ett bytesförslag till den här personen."
        ))
    except Trade.DoesNotExist:
        pass

    try:
        Trade.get_active(sender=receiver, receiver=request.user)

        return render(request, "400.html", dict(
            exception="Den här användaren har redan skickat en bytesförfrågan till dig. "
                      "Svara på den innan du skickar en ny förfrågan."
        ))
    except Trade.DoesNotExist:
        pass

    if request.method == "POST":
        form = TradeForm(sender=request.user, receiver=receiver, data=request.POST)

        if form.is_valid():
            # At this point I could just as well just initialize an empty instance,
            # but for future compatibility I'll leave it like this.
            trade = form.save(commit=False)

            trade.sender = request.user
            trade.receiver = receiver

            # Apparently a model instance must be saved (acquire an ID) before M2M relations can be set.
            # Therefore, two saves are required.
            trade.save()

            trade.sent.set(form.cleaned_data.get("sent"))
            trade.requested.set(form.cleaned_data.get("requested"))

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
        trade = Trade.get_active(sender=sender, receiver=request.user)
    except Trade.DoesNotExist:
        raise Http404("Bytesförfrågan hittades ej. Sändaren kan ha avbrutit förfrågan.")

    if request.method == "POST":
        accepted = "true" in request.POST.get("accept", [])

        trade.apply(accepted=accepted)

        return render(request, "trade/confirmation.html", dict(
            sender=sender,
            accepted=accepted
        ))
    else:
        return render(request, "trade/complete.html", dict(
            sender=sender,
            trade=trade,
        ))
