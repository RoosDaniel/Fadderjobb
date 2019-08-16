from django import forms

from fadderanmalan.models import Job, JobUser
from fadderanmalan.utils import misc as misc_utils

from .models import Trade


# This is a custom iterator allowing a custom render of the object. The default implementation doesn't include the
# object itself.
class CustomModelChoiceIterator(forms.models.ModelChoiceIterator):
    def choice(self, obj):
        return obj


# In order to apply the custom iterator the entire field has to be sub-classed
class CustomModelChoiceField(forms.models.ModelMultipleChoiceField):
    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices
        return CustomModelChoiceIterator(self)

    choices = property(_get_choices,
                       forms.MultipleChoiceField._set_choices)


class TradeForm(forms.ModelForm):
    class Meta:
        model = Trade
        fields = ("requested", "sent")

    def __init__(self, sender, receiver, *args, **kwargs):
        super(TradeForm, self).__init__(*args, **kwargs)

        self.label_suffix = ""
        self.sender = sender
        self.receiver = receiver

        sender_jobs = sender.jobs.exclude(id__in=receiver.jobs.values_list('id', flat=True))
        sender_jobs = misc_utils.filter_jobs_for_user(receiver, sender_jobs)

        receiver_jobs = receiver.jobs.exclude(id__in=sender.jobs.values_list('id', flat=True))
        receiver_jobs = misc_utils.filter_jobs_for_user(sender, receiver_jobs)

        self.fields["requested"] = CustomModelChoiceField(
            queryset=receiver_jobs,
            label="Deras jobb",
            widget=forms.CheckboxSelectMultiple(),
            required=False,
        )

        self.fields["sent"] = CustomModelChoiceField(
            queryset=sender_jobs,
            label="Dina jobb",
            widget=forms.CheckboxSelectMultiple(),
            required=False,
        )

    def clean(self):
        # For a reason I cannot explain, this happens when a user tries to start a trade using jobs that either party
        # are not registered to. I also added the for-loops below as a safety-measure, since I don't trust this
        # behavior.
        if "sent" not in self.cleaned_data or "requested" not in self.cleaned_data:
            raise forms.ValidationError("Något gick fel, troligtvis har du eller %s avregistrerat sig på något "
                                        "av jobben som inkluderades i bytet." % self.receiver,
                                        code="unknown_error")

        # Check that at least one job is included in the trade
        if not (self.cleaned_data["sent"] or self.cleaned_data["requested"]):
            raise forms.ValidationError("Inga jobb valda.",
                                        code="no_jobs")

        # Check that sender is registered to all sent jobs
        for job in self.cleaned_data.get("sent").all():
            try:
                JobUser.get(job, self.sender)
            except JobUser.DoesNotExist:
                raise forms.ValidationError("Du är inte registrerad på jobbet %s." % job,
                                            code="sender_not_registered")

        # Check that receiver is registered to all requested jobs
        for job in self.cleaned_data.get("requested").all():
            try:
                JobUser.get(job, self.receiver)
            except JobUser.DoesNotExist:
                raise forms.ValidationError("%s är inte längre registrerad på jobbet %s." % (self.receiver, job),
                                            code="receiver_not_registered")
