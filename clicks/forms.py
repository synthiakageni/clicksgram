from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import fields
from . models import Image, Profile
from .models import Profile
from django.forms import ModelForm
class RegistrationForm(UserCreationForm):
    barua = forms.EmailField()
    class Meta:
        model = User
        fields = ['username','first_name','email'] #primary att for the user are username,password,email,first_name and last_name
class UpdateProfileForm(ModelForm):
    """A form for updating/editing user profile"""

    class meta:
        model = Image
        fields = '__all__'
        exclude = ['likes', 'user']
