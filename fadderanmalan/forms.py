from django import forms


class TradeForm(forms.Form):
    def __init__(self, sender, receiver, *args, **kwargs):
        super(TradeForm, self).__init__(*args, **kwargs)

        self.fields["sender_jobs"] = forms.ModelMultipleChoiceField(
            queryset=sender.jobs.exclude(id__in=receiver.jobs.values_list('id', flat=True)),
            label="Dina jobb",
            widget=forms.CheckboxSelectMultiple(),
            required=False,
        )

        self.fields["receiver_jobs"] = forms.ModelMultipleChoiceField(
            queryset=receiver.jobs.exclude(id__in=sender.jobs.values_list('id', flat=True)),
            label="Deras jobb",
            widget=forms.CheckboxSelectMultiple(),
            required=False,
        )

    def clean(self):
        if not (self.cleaned_data["sender_jobs"] or self.cleaned_data["receiver_jobs"]):
            raise forms.ValidationError("Inga jobb valda.", code="no_jobs")
