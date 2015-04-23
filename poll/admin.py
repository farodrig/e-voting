__author__ = 'farodrig'

from models import Poll, Question, Vote
from django.contrib import admin

admin.site.register(Poll)
admin.site.register(Question)
admin.site.register(Vote)