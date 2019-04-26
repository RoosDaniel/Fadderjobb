from django import forms

from .models import Trade
from fadderanmalan.models import JobUser


class CustomModelChoiceIterator(forms.models.ModelChoiceIterator):
    def choice(self, obj):
        return obj


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

        sender_jobs = JobUser.objects.filter(user=sender)\
            .exclude(job__id__in=receiver.jobs.values_list('id', flat=True))

        receiver_jobs = JobUser.objects.filter(user=receiver)\
            .exclude(job__id__in=sender.jobs.values_list('id', flat=True))

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
        if not (self.cleaned_data["sent"] or self.cleaned_data["requested"]):
            raise forms.ValidationError("Inga jobb valda.", code="no_jobs")
