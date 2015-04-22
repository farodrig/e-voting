__author__ = 'farodrig'

from django.conf.urls import include, url
from . import views

urlpatterns = [
    # Examples:
    url(r'^$', views.main),
    url(r'^signin/$', views.validate),
    url(r'^logout/$', views.out),
#    url(r'^signup$', views.register),
]
