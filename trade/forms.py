from django import forms

from .models import Trade
from fadderanmalan.models import JobUser


class TradeForm(forms.ModelForm):
    class Meta:
        model = Trade
        fields = ("sent", "requested")

    def __init__(self, sender, receiver, *args, **kwargs):
        super(TradeForm, self).__init__(*args, **kwargs)

        sender_jobs = JobUser.objects.filter(user=sender)\
            .exclude(job__id__in=receiver.jobs.values_list('id', flat=True))

        receiver_jobs = JobUser.objects.filter(user=receiver)\
            .exclude(job__id__in=sender.jobs.values_list('id', flat=True))

        self.fields["sent"] = forms.ModelMultipleChoiceField(
            queryset=sender_jobs,
            label="Dina jobb",
            widget=forms.CheckboxSelectMultiple(),
            required=False,
        )

        self.fields["requested"] = forms.ModelMultipleChoiceField(
            queryset=receiver_jobs,
            label="Deras jobb",
            widget=forms.CheckboxSelectMultiple(),
            required=False,
        )

    def clean(self):
        if not (self.cleaned_data["sent"] or self.cleaned_data["requested"]):
            raise forms.ValidationError("Inga jobb valda.", code="no_jobs")
