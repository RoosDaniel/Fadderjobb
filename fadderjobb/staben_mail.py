from django.core.mail import send_mail as django_send_mail


def send_mail(recipient, subject, message):
    django_send_mail("Fadderjobb - " + subject, message,
                     "STABEN Noreply <noreply@staben.info>", [recipient], fail_silently=True)
