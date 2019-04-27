from post_office import mail
from webpush import send_user_notification


def send_mail(recipient, subject, message):
    mail.send(
        recipient,
        "STABEN NOREPLY <noreply@staben.info>",
        subject="Fadderjobb - " + subject,
        message=message
    )


def send_push(user, subject, message, push_link=None):
    payload = dict(
        head=subject,
        body=message,
    )

    if push_link is not None:
        payload.update(url=push_link)

    send_user_notification(user=user, payload=payload, ttl=1000)


def notify_user(user, subject, message, push_link=None):
    send_mail(user.email, subject, message)
    send_push(user, subject, message, push_link)
