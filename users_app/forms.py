from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email:', max_length=100)
    password = forms.CharField(
        widget=forms.PasswordInput(),
        max_length=128,
        required=True,
    )
