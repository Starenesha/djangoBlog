from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms

from .models import User


class AuthUserForm(AuthenticationForm, forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'password')


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=150)
    password1 = forms.CharField(max_length=20, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=20, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')


class LoginForm(forms.Form):
    email = forms.CharField(label = "email")
    password = forms.CharField(label = "Password", widget = forms.PasswordInput)