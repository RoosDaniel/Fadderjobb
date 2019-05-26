from django.template import Template, Context

from post_office import mail
from post_office.models import EmailTemplate

from webpush import send_user_notification


def send_mail(recipient, subject, message, html_message):
    mail.send(
        recipient,
        "STABEN NOREPLY <noreply@staben.info>",
        subject="Fadderjobb - " + subject,
        message=message,
        html_message=html_message
    )


def send_push(user, subject, message, push_link=None):
    payload = dict(
        head=subject,
        body=message,
    )

    if push_link is not None:
        payload.update(url=push_link)

    send_user_notification(user=user, payload=payload, ttl=1000)


def notify_user(user, subject=None, message=None, html_message=None, template=None, template_context=None,
                push_link=None):
    if template is not None:
        template = EmailTemplate.objects.get(name=template)
        context = Context(template_context or {})

        subject = Template(template.subject).render(context)
        message = Template(template.content).render(context)
        html_message = Template(template.html_content).render(context)
    elif subject is None:
        raise Exception("Neither subject nor template supplied. "
                        "If not using a template, you should also include a message.")

    send_mail(user.email, subject, message, html_message)
    send_push(user, subject, message, push_link)
