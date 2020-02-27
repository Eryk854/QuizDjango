from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Account, Player

class RegisterForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ['email', 'password1', 'password2']

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['username','profile_image']


