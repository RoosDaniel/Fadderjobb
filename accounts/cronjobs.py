from uwsgidecorators import cron

from .models import User
from .utils import update_user_placings


@cron(0, 0, -1, -1, -1)
def update_points(num):
    for user in User.objects.filter(is_staff=False):
        user.update_points()
        print(user)
    update_user_placings()
