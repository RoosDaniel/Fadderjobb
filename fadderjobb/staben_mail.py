from post_office import mail


def send_mail(recipient, subject, message):
    mail.send(
        recipient,
        "STABEN NOREPLY <noreply@staben.info>",
        subject="Fadderjobb - " + subject,
        message=message
    )
