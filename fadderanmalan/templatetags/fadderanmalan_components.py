from django import template

register = template.Library()


@register.inclusion_tag("components/job.html", takes_context=True)
def job_component(context, job):
    context.update(dict(job=job))

    return context


@register.inclusion_tag("components/equipment_ownership.html", takes_context=True)
def equipment_ownership_component(context, equipment_ownership):
    context.update(dict(eo=equipment_ownership))

    return context


@register.inclusion_tag("components/filter_checkbox.html")
def filter_checkbox_component(label, id, prev):

    return dict(label=label, id=id, prev=prev)
