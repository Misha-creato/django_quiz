from django.contrib.auth.forms import (
    UserCreationForm,
)

from django import forms

from users.models import CustomUser as User


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
    )

    class Meta:
        model = User
        fields = (
            'email',
            'password1',
            'password2',
        )
