from django.shortcuts import render

from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.db.models.functions import Coalesce

User = get_user_model()


def index(request):
    search = request.GET.get("search", "")

    users = User.objects.filter(is_staff=False).order_by("placing").all()

    if search != "":
        name_filtered = users.filter(name__icontains=search)
        username_filtered = users.filter(username__icontains=search)
        users = name_filtered.union(username_filtered)

    return render(request, "topchart/index.html", dict(
        users=users,
        filter_search=search
    ))
