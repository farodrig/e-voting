#encoding:utf-8

__author__ = 'farodrig'

from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label = "Contraseña")
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
