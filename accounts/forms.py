import re

from django import forms

from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget as PhoneWidget


class FadderEditForm(forms.Form):
    email = forms.EmailField(label="Epost", required=True,
                             widget=forms.EmailInput(attrs={"class": "form-control"}))

    phone_number = PhoneNumberField(label="Telefonnummer", required=False,
                                    widget=PhoneWidget(attrs={"class": "form-control"}))

    motto = forms.CharField(label="Motto", required=False,
                            widget=forms.Textarea(attrs={"class": "form-control", "maxlength": 100, "rows": 3}))
