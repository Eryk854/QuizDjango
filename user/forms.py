from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Account

class RegisterForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ['email','username','password1','password2']

