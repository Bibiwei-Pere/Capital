from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *


class CustomUserCreationForm(UserCreationForm):
    username  = forms.CharField()
    password1 = forms.CharField(widget = forms.PasswordInput, label='Password',
    help_text='min_lenght-8 mix characters [i.e alex1234] ')
    password2 = forms.CharField(widget = forms.PasswordInput,help_text='Enter same password as before',label='Confirm Password')
    Phone = forms.CharField(max_length = 11, min_length = 11)
    referer_username = forms.CharField(required=False,help_text='Leave blank if no referral',label='Referral username [optional]')

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("FullName",'username','email','Phone','Address','referer_username','password1','password2')
