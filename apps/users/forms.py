from django.contrib.auth.forms import (
    UserCreationForm,
)

from django import forms

from users.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
    )

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'password1',
            'password2',
        )


class LoginForm(forms.Form):
    email = forms.EmailField(
        required=True,
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
    )


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(
        required=True,
    )
