from .models import User
from django.conf import settings


def _get_user(tree):
    username = tree[0][0].text
    user, _ = User.objects.get_or_create(username=username)
    return user


def add_email(tree):
    user = _get_user(tree)
    user.email = "%s@student.liu.se" % user.username
    user.save()


def set_admin(tree):
    user = _get_user(tree)
    if user.username in settings.SYSTEM_ADMINS:
        user.is_staff = True
        user.is_superuser = True
        user.save()
