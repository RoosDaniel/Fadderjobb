from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from fadderanmalan.models import Job, EnterQueue, LeaveQueue


# TODO Email notifications for dequeueing.
# If an admin wishes to move a user they have to manage the queues manually.


@login_required(login_url="accounts:login")
def register_for_job(request, job_id):
    job = Job.objects.get(id=job_id)

    if request.method == "POST":
        if job.full():
            try:  # First try removing ourselves from the lq if we changed our mind
                lq = LeaveQueue.objects.get(job=job, user=request.user)
                lq.delete()

                messages.add_message(request, messages.INFO,
                                     "Din köplats är nu borttagen.")
            except LeaveQueue.DoesNotExist:  # We weren't queued to leave, try to register us
                try:  # If someone else wants to leave, take their slot
                    lq = LeaveQueue.get_first(job=job)
                    lq.apply()
                    job.users.add(request.user)

                    messages.add_message(request, messages.INFO,
                                         "Du är nu registrerad på passet. Du tog %s:s plats." % lq.user.username)
                except LeaveQueue.DoesNotExist:  # No one wanted to leave, queue us for enter
                    eq = EnterQueue(job=job, user=request.user)
                    eq.save()

                    messages.add_message(request, messages.INFO,
                                         "Du står nu i kö för passet. "
                                         "Om en fadder lämnar passet kommer du att få det.")
        else:  # Not full, just register
            job.users.add(request.user)

            messages.add_message(request, messages.INFO,
                                 "Du är nu registrerad för passet.")

    return redirect("fadderanmalan:jobsignup_detail", job.slug)


@login_required(login_url="accounts:login")
def deregister_for_job(request, job_id):
    job = Job.objects.get(id=job_id)

    if request.method == "POST":
        try:  # First try removing ourselves from the eq
            eq = EnterQueue.objects.get(job=job, user=request.user)
            eq.delete()

            messages.add_message(request, messages.INFO,
                                 "Din köplats är nu borttagen.")
        except EnterQueue.DoesNotExist:  # We were not in the eq
            if job.locked:
                try:  # If someone else wants to enter, give the slot to them
                    eq = EnterQueue.get_first(job=job)
                    job.users.remove(request.user)
                    eq.apply()

                    messages.add_message(request, messages.INFO,
                                         "Du är nu avregistrerad från passet. %s tog din plats."
                                         % eq.user.username)
                except EnterQueue.DoesNotExist:  # No one wanted to enter, queue us for leave
                    lq = LeaveQueue(job=job, user=request.user)
                    lq.save()

                    messages.add_message(request, messages.INFO,
                                         "Du står nu i kö för att avregistrera dig från passet. "
                                         "Om en fadder ställer sig i kön för passet kommer denna att ta din plats.")
            else:
                job.users.remove(request.user)
                message = "Du är nu avregistrerad från passet."

                try:  # If there is someone queued, give the slot to them
                    eq = EnterQueue.get_first(job=job)
                    eq.apply()

                    message += " %s tog din plats." % eq.user.username
                except EnterQueue.DoesNotExist:
                    pass

                messages.add_message(request, messages.INFO, message)

    return redirect("fadderanmalan:jobsignup_detail", job.slug)
