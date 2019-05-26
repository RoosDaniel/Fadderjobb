from django.shortcuts import render

from django.contrib.auth import get_user_model
from django.db.models import Sum


User = get_user_model()


def index(request):
    users = User.objects.annotate(points=Sum("jobs__points"))\
        .filter(is_staff=False).order_by("points").all()

    return render(request, "topchart/index.html", dict(
        users=users,
    ))
