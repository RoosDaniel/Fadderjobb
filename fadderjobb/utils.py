from django.template import Template, Context
from django.contrib.auth.models import Group

from post_office import mail
from post_office.models import EmailTemplate

from accounts.models import User


def send_mail(recipient, subject, message, html_message):
    mail.send(
        recipient,
        "STABEN NOREPLY <noreply@staben.info>",
        subject="Fadderjobb - " + subject,
        message=message,
        html_message=html_message
    )


def _build_message(template_name, template_context):
    template = EmailTemplate.objects.get(name=template_name)
    context = Context(template_context or {})

    subject = Template(template.subject).render(context)
    message = Template(template.content).render(context)
    html_message = Template(template.html_content).render(context)

    return subject, message, html_message


def notify_user(user, subject=None, message=None, html_message=None, template=None, template_context=None):
    if template is not None:
        subject, message, html_message = _build_message(template, template_context)
    elif subject is None:
        raise Exception("Neither subject nor template supplied. "
                        "If not using a template, you should also include a message.")

    send_mail(user.email, subject, message, html_message)


def notify_group(group_name, subject=None, message=None, html_message=None, template=None, template_context=None):
    if template is not None:
        subject, message, html_message = _build_message(template, template_context)
    elif subject is None:
        raise Exception("Neither subject nor template supplied. "
                        "If not using a template, you should also include a message.")

    users = Group.objects.get(name=group_name).user_set.all()

    for user in users:
        send_mail(user.email, subject, message, html_message)
