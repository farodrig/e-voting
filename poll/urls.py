__author__ = 'farodrig'

from django.conf.urls import include, url
from . import views

urlpatterns = [
    # Examples:
    url(r'^$', views.main),
    url(r'^signin/$', views.validate),
    url(r'^logout/$', views.out),
    url(r'^createpoll/$', views.createPoll),
    url(r'^signup$', views.register),
    url(r'^poll_list$', views.poll_list),
    url(r'^invitation_list$', views.invitation_list),
    url(r'^poll_results', views.results),
	url(r'^createquestion/$', views.createQuestion, name="createquestion"),
	url(r'^search$', views.search),
]
