from django import template

from ..utils import misc as misc_utils

register = template.Library()


@register.filter('startswith')
def startswith(text, starts):
    if isinstance(text, str):
        return text.startswith(starts)
    return False


@register.filter('filter_jobs_for_user')
def filter_jobs_for_user(user, jobs):
    return misc_utils.filter_jobs_for_user(user, jobs)
