from django.db import models
from cart.models import Usuario, Delivery
from datetime import datetime

class User(models.Model):
	email = models.CharField(max_length=50, null=False, unique = True)
	password = models.CharField(max_length=50, null=False)
	name = models.CharField(max_length=50, null=False)
	lastname = models.CharField(max_length=50, null=False)
	def __unicode__(self):
		return self.name + ' ' + self.lastname

class Votation(models.Model):
	PRIVACY_STATUS = (
        ('P', 'Public'),
        ('C', 'Closed'),
    )
    guests = models.ManyToMany(User)
	privacy_status = models.CharField(max_length=1, choices=PRIVACY_STATUS)
	owner=models.ForeignKey(User)
	name=models.CharField(max_length=50, blank=True)
	init_date = models.DateTimeField(null=False)
	close_date = models.DateTimeField(null=False)
	def __unicode__(self):

class Question(models.Model):
	votation=models.ForeignKey(Votation)
	question = models.CharField(max_length=50, null=False)
	def __unicode__(self):

class Vote(models.Model):
	question=models.ForeignKey(Question)
	voter= models.ForeignKey(User)
	vote_value=models.CharField()
	def __unicode__(self):