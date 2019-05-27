from django.shortcuts import render

from django.contrib.auth import get_user_model
from django.db.models import Sum


User = get_user_model()


def index(request):
    search = request.GET.get("search", "")

    users = User.objects.annotate(points=Sum("jobs__points"))\
        .filter(is_staff=False).order_by("points").all()

    placings = {u.username: placing+1 for placing, u in enumerate(users)}

    if search != "":
        name_filtered = users.filter(name__icontains=search)
        username_filtered = users.filter(username__icontains=search)
        users = name_filtered.union(username_filtered)

    usernames = users.values_list('username', flat=True)
    placings = [placing for username, placing in placings.items() if username in usernames]

    return render(request, "topchart/index.html", dict(
        users_and_placings=zip(users, placings),
        filter_search=search
    ))
