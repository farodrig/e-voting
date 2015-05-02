#encoding:utf-8

__author__ = 'farodrig'

from django.contrib.auth.models import User
from models import Poll
from django import forms

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label = "Contraseña")
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

class PollForm(forms.ModelForm):
    #password = forms.CharField(widget=forms.PasswordInput(), label = "Contraseña")
    class Meta:
        model = Poll
        fields = ('name', 'init_date', 'close_date', 'privacy_status')
