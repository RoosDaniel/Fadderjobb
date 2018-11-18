from django import template

register = template.Library()


@register.inclusion_tag("components/userlink.html")
def userlink(user):
    return {"user": user}
