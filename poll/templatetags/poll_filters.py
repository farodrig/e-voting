__author__ = 'farodrig'
from django import template
from django.utils import timezone
register = template.Library()

@register.filter(name='past')
def past(value):
    if value<timezone.now():
        return True
    return False

