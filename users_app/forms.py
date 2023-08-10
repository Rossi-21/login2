from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email:', max_length=100)
    password = forms.CharField(
        widget=forms.PasswordInput(),
        max_length=128,
        required=True,
    )


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
