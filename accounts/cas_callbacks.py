from django.contrib.auth import get_user_model

from django.conf import settings


User = get_user_model()


def _get_user(tree):
    username = tree[0][0].text.lower()

    # This will throw an exception if the user isn't found, which is fine since we have a whitelist
    return User.objects.get(username__iexact=username)


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
