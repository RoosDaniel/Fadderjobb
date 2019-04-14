from django.shortcuts import render
from django.contrib.auth import get_user_model

from .forms import TradeForm


User = get_user_model()


def trade(request, receiver_username):
    receiver = User.objects.get(username=receiver_username)

    if request.method == "POST":
        form = TradeForm(sender=request.user, receiver=receiver, data=request.POST)

        if form.is_valid():
            messages.add_message(request, messages.INFO,
                                 "Bytesförfrågan har skickats på mail till %s." % receiver.username)
        else:
            messages.add_message(request, messages.ERROR,
                                 "Ett eller flera problem uppstod.")
    else:
        form = TradeForm(sender=request.user, receiver=receiver)

    return render(request, "trade/index.html", dict(
        trade_form=form,
        receiver=receiver,
    ))
