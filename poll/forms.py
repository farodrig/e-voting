#encoding:utf-8

__author__ = 'farodrig'

from django.contrib.auth.models import User
from poll import models
from django import forms

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label = "Contraseña")
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

class PollForm(forms.ModelForm):
    class Meta:
        model = models.Poll
        exclude = ('creator',)

class QuestionForm(forms.ModelForm):
	class Meta:
		model = models.Question
		exclude = ('poll','type')
class AnswerForm(forms.ModelForm):
	class Meta:
		model = models.Answer
		exclude = ('question',)