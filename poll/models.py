from django.db import models
from django.contrib.auth.models import User

class Poll(models.Model):
    PRIVACY_STATUS = (
        ('P', 'Public'),
        ('C', 'Closed'),
    )
    creator = models.ForeignKey(User)
    privacy_status = models.CharField(max_length=1, choices=PRIVACY_STATUS)
    name = models.CharField(max_length=50, blank=True)
    init_date = models.DateTimeField(null=False)
    close_date = models.DateTimeField(null=False)
    def __unicode__(self):
        return

class Invitation(models.Model):
    poll = models.ForeignKey(Poll)
    guest = models.ForeignKey(User)

class Question(models.Model):
    votation = models.ForeignKey(Poll)
    question = models.CharField(max_length=50, null=False)
    def __unicode__(self):
        return

class Vote(models.Model):
    question = models.ForeignKey(Question)
    voter = models.ForeignKey(User)
    vote_value = models.CharField(max_length=10)
    def __unicode__(self):
        return