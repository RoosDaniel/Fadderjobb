from django import template

register = template.Library()


@register.inclusion_tag("components/job.html")
def job_component(job):
    return {"job": job}


@register.inclusion_tag("components/filter_checkbox.html")
def filter_checkbox_component(label, id, prev):
    return {"label": label, "id": id, "prev": prev}
