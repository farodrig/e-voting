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
    name = models.CharField(max_length=100, null=False)
    def __unicode__(self):
        return self.poll.name + " - " + self.name

#La idea seria que aqui fueran los tipos de los input para el html, o asi lo pense, siempre se puede cambiar
class Type(models.Model):
    name = models.CharField(max_length=30)
    def __unicode__(self):
        return self.name

class Answer(models.Model):
    question = models.ForeignKey(Question)
    type = models.ForeignKey(Type)
    name = models.CharField(max_length=30) #la idea es q sea el nombre del tag name del html
    value = models.CharField(max_length=200, blank=True)
    def __unicode__(self):
        return self.question.name + " - " + self.value

class Vote(models.Model):
    answer = models.ForeignKey(Answer)
    voter = models.ForeignKey(User)
    value = models.CharField(max_length=100, blank=True)
    def __unicode__(self):
        return self.answer.value + ": " + self.value