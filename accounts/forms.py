import re

from django import forms


class FadderEditForm(forms.Form):
    motto = forms.CharField(label="Motto", required=False,
                            widget=forms.Textarea(attrs={"class": "form-control", "maxlength": 100, "rows": 3}))

    phone_number = forms.IntegerField(label="Telefonnummer",
                                      widget=forms.NumberInput(attrs={"class": "form-control"}))
