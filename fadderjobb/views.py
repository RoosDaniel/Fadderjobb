from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def index(request):
    return render(request, "index.html")


@login_required
def guide(request):
    if request.method == "GET":
        return render(request, "guide.html")

    elif request.method == "POST":
        if "accept" in request.POST:
            request.user.read_guide = True
            request.user.save()

            messages.add_message(request, messages.INFO, "Du har nu markerat att du har läst guiden. Bra jobbat!")

            return redirect("index")
