from django.contrib import messages
from django.shortcuts import render

from fadderanmalan.models import JobUser, EnterQueue, LeaveQueue
from fadderanmalan.exceptions import UserError


def handle_register(request, job):
    # Simply register the user to the job
    if "_register" in request.POST:
        if job.full():
            raise UserError("Du kan inte registrera dig.")

        try:
            JobUser.get(job, request.user)
        except JobUser.DoesNotExist:
            JobUser.create(job, request.user)

        messages.add_message(request, messages.INFO,
                             "Du är nu registrerad på passet.")

    # Simply deregister the user from the job
    elif "_deregister" in request.POST:
        if job.is_locked():
            raise Exception("Du kan inte avregistrera dig.")

        JobUser.remove(job, request.user)
        message = "Du är nu avregistrerad från passet."

        try:  # If there is someone queued, give the slot to them
            eq = EnterQueue.get_first(job=job)
            eq.apply()

            message += " %s tog din plats." % eq.user.username
        except EnterQueue.DoesNotExist:  # Else, just ignore it
            pass

        messages.add_message(request, messages.INFO, message)

    # Put the user in the leave queue
    elif "_add_lq" in request.POST:
        try:
            LeaveQueue.objects.get(job=job, user=request.user)
        except LeaveQueue.DoesNotExist:
            lq = LeaveQueue(job=job, user=request.user)
            lq.save()

        messages.add_message(request, messages.INFO,
                             "Du står nu i kö för att avregistrera dig från passet. "
                             "Om en fadder ställer sig i kön för passet kommer denna att ta din plats.")

    # Put the user in the enter queue
    elif "_add_eq" in request.POST:
        try:
            EnterQueue.objects.get(job=job, user=request.user)
        except EnterQueue.DoesNotExist:
            eq = EnterQueue(job=job, user=request.user)
            eq.save()

        messages.add_message(request, messages.INFO,
                             "Du står nu i kö för passet. "
                             "Om en fadder lämnar passet kommer du att få det.")

    # The user longer want to queue to leave the job
    elif "_remove_lq" in request.POST:
        try:
            lq = LeaveQueue.objects.get(job=job, user=request.user)
            lq.delete()

            messages.add_message(request, messages.INFO,
                                 "Din köplats är nu borttagen.")
        except LeaveQueue.DoesNotExist:
            raise UserError("Du var inte köad för att lämna jobbet.")

    # Remove the user from the enter queue
    elif "_remove_eq" in request.POST:
        try:
            eq = EnterQueue.objects.get(job=job, user=request.user)
            eq.delete()

            messages.add_message(request, messages.INFO,
                                 "Din köplats är nu borttagen.")
        except EnterQueue.DoesNotExist:
            raise UserError("Du var inte köad för att gå med i jobbet.")

    # Someone else wants to enter, give the slot to them and deregister the user
    elif "_take_other_eq" in request.POST:
        try:
            eq = EnterQueue.get_first(job=job)
            JobUser.remove(job, request.user)
            eq.apply()

            messages.add_message(request, messages.INFO,
                                 "Du är nu avregistrerad från passet. %s tog din plats."
                                 % eq.user.username)
        except EnterQueue.DoesNotExist:
            raise UserError("Ingen annan köade för att registrera sig på jobbet.")

    # Someone else wants to leave, take their slot
    elif "_take_other_lq" in request.POST:
        try:
            lq = LeaveQueue.get_first(job=job)
            lq.apply()
            JobUser.create(job, request.user)

            messages.add_message(request, messages.INFO,
                                 "Du är nu registrerad på passet. Du tog %s:s plats."
                                 % lq.user.username)
        except LeaveQueue.DoesNotExist:
            raise UserError("Ingen annan köade för att avregistrera sig från jobbet.")


def generate_registration_text(request, job):
    try:
        JobUser.get(job, request.user)
        registered_to_job = True
    except JobUser.DoesNotExist:
        registered_to_job = False

    try:
        LeaveQueue.objects.get(user=request.user, job=job)
        queued_to_leave = True
    except LeaveQueue.DoesNotExist:
        queued_to_leave = False

    try:
        EnterQueue.objects.get(user=request.user, job=job)
        queued_to_enter = True
    except EnterQueue.DoesNotExist:
        queued_to_enter = False

    if registered_to_job:
        if job.is_locked():
            if queued_to_leave:
                return (
                    "Du står i kö för att avanmäla dig från det här jobbet. Vill du ta bort din köplats?",
                    "Ta bort min köplats",
                    "_remove_lq"
                )
            else:
                if job.has_enter_queue():
                    return (
                        "Avanmälan till det här jobbet har stängt, men det finns faddrar som vill ta din plats.",
                        "Ge bort min plats",
                        "_take_other_eq"
                    )
                else:
                    return (
                        "Avanmälan till det här jobbet har stängt. Du kan ställa dig i kön till att avregistrera dig.",
                        "Ställ mig i kön",
                        "_add_lq"
                    )
        else:
            return (
                "",
                "Avanmäl mig",
                "_deregister"
            )
    else:
        if job.full():
            if queued_to_enter:
                return (
                    "Du står i kö till jobbet. Vill du ta bort din köplats?",
                    "Ta bort min köplats",
                    "_remove_eq"
                )
            else:
                if job.has_leave_queue():
                    return (
                        "Jobbet är fullsatt, men det finns faddrar som vill lämna passet.",
                        "Ta en plats",
                        "_take_other_lq"
                    )
                else:
                    return (
                        "Jobbet är fullsatt. Du kan ställa dig i kö till jobbet.",
                        "Ställ mig i kön",
                        "_add_eq"
                    )
        else:
            return (
                "",
                "Anmäl mig",
                "_register"
            )
