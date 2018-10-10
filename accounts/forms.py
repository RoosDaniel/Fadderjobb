import re

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms


class FadderCreationForm(UserCreationForm):
    username = forms.CharField(label="Liu id", max_length=8,
                               widget=forms.TextInput(attrs={"class": "form-control"}))

    email = forms.EmailField(label="Email",
                             widget=forms.EmailInput(attrs={"class": "form-control"}))

    password1 = forms.CharField(label="Lösenord",
                                widget=forms.PasswordInput(attrs={"class": "form-control"}))

    password2 = forms.CharField(label="Upprepa lösenord",
                                widget=forms.PasswordInput(attrs={"class": "form-control"}))

    field_order = [
        "username",
        "email"
    ]

    def clean_username(self):
        username = self.cleaned_data["username"]

        if not re.match(r"[a-zA-Z]{5}[0-9]{3}", username):
            raise forms.ValidationError("Not a liu id.")

        return username


class FadderLoginForm(AuthenticationForm):
    username = forms.CharField(label="Liu id", max_length=8,
                               widget=forms.TextInput(attrs={"class": "form-control"}))

    password = forms.CharField(label="Lösenord",
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))

    def clean_username(self):
        username = self.cleaned_data["username"]

        if not re.match(r"[a-zA-Z]{5}[0-9]{3}", username):
            raise forms.ValidationError("Not a liu id.")

        return username
