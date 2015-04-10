from django.db import models
from django.contrib.auth.models import User


class Poll(models.Model):
    PRIVACY_STATUS = (
        ('P', 'Public'),
        ('C', 'Closed'),
    )
    guests = models.ManyToManyField(User, through='Membership', through_fields=('poll', 'member'))
    privacy_status = models.CharField(max_length=1, choices=PRIVACY_STATUS)
    name = models.CharField(max_length=50, blank=True)
    init_date = models.DateTimeField(null=False)
    close_date = models.DateTimeField(null=False)
    def __unicode__(self):
        return

class Membership(models.Model):
    poll = models.ForeignKey(Poll)
    member = models.ForeignKey(User)
    inviter = models.ForeignKey(User, related_name="membership_invites")

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