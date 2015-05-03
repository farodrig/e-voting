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
        return unicode(self.name) + ' - ' + unicode(self.creator)


class Invitation(models.Model):
    poll = models.ForeignKey(Poll)
    guest = models.ForeignKey(User)
    answered = models.BooleanField(default=False)
    def __unicode__(self):
        return self.poll.name + " - " + self.guest

class Question(models.Model):
    poll = models.ForeignKey(Poll)
    question = models.CharField(max_length=50, null=False)
    def __unicode__(self):
        return self.poll + " - " + self.question

class Vote(models.Model):
    question = models.ForeignKey(Question)
    voter = models.ForeignKey(User)
    value = models.CharField(max_length=10)
    def __unicode__(self):
        return self.question + ": " + self.value