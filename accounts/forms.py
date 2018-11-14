import re

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model

from django.contrib import messages
from django import forms


User = get_user_model()


class FadderEditForm(forms.Form):
    current_password = forms.CharField(label="Nuvarande lösenord", required=False,
                                       widget=forms.PasswordInput(attrs={
                                           "class": "form-control", "placeholder": "Måste anges vid ändringar"
                                       }))

    email = forms.EmailField(label="Email", required=False,
                             widget=forms.EmailInput(attrs={"class": "form-control"}))

    motto = forms.CharField(label="Motto", required=False,
                            widget=forms.Textarea(attrs={"class": "form-control", "maxlength": 100, "rows": 3}))

    password1 = forms.CharField(label="Nytt lösenord", required=False,
                                widget=forms.PasswordInput(attrs={"class": "form-control"}))

    password2 = forms.CharField(label="Upprepa lösenord", required=False,
                                widget=forms.PasswordInput(attrs={"class": "form-control"}))

    def __init__(self, user, **kwargs):
        super().__init__(**kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get("password1") != cleaned_data.get("password2"):
            raise forms.ValidationError("Lösenorden stämmer inte överens.")

    def clean_current_password(self):
        password = self.cleaned_data.get("current_password")
        if not self.user.check_password(password):
            raise forms.ValidationError("Fel lösenord.")

    def clean_password1(self):
        new_password = self.cleaned_data.get("password1")

        if new_password:
            validate_password(new_password, user=self.user)


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

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

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

    class Meta:
        model = User
        fields = ["username", "password"]

    def clean_username(self):
        username = self.cleaned_data["username"]

        if not re.match(r"[a-zA-Z]{5}[0-9]{3}", username):
            raise forms.ValidationError("Not a liu id.")

        return username
