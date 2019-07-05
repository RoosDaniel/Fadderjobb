from .models import User


def update_user_placings():
    users = User.objects.filter(is_staff=False).order_by("-points").all()

    for i, user in enumerate(users):
        user.placing = i+1

    User.objects.bulk_update(users, ["placing"], batch_size=20)
