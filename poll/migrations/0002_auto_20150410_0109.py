# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='inviter',
            field=models.ForeignKey(related_name='membership_invites', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='membership',
            name='member',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='poll',
            name='guests',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='poll.Membership'),
        ),
        migrations.AlterField(
            model_name='vote',
            name='voter',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
