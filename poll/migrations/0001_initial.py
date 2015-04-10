# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('privacy_status', models.CharField(max_length=1, choices=[(b'P', b'Public'), (b'C', b'Closed')])),
                ('name', models.CharField(max_length=50, blank=True)),
                ('init_date', models.DateTimeField()),
                ('close_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.CharField(max_length=50)),
                ('votation', models.ForeignKey(to='poll.Poll')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.CharField(unique=True, max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vote_value', models.CharField(max_length=10)),
                ('question', models.ForeignKey(to='poll.Question')),
                ('voter', models.ForeignKey(to='poll.User')),
            ],
        ),
        migrations.AddField(
            model_name='poll',
            name='guests',
            field=models.ManyToManyField(to='poll.User', through='poll.Membership'),
        ),
        migrations.AddField(
            model_name='membership',
            name='inviter',
            field=models.ForeignKey(related_name='membership_invites', to='poll.User'),
        ),
        migrations.AddField(
            model_name='membership',
            name='member',
            field=models.ForeignKey(to='poll.User'),
        ),
        migrations.AddField(
            model_name='membership',
            name='poll',
            field=models.ForeignKey(to='poll.Poll'),
        ),
    ]
