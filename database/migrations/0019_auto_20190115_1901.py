# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2019-01-15 19:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0018_participantsurvey'),
    ]

    operations = [
        migrations.AddField(
            model_name='participantsurvey',
            name='name',
            field=models.TextField(help_text='Name of the study; can be of any length', null=True),
        ),
        migrations.AddField(
            model_name='survey',
            name='name',
            field=models.TextField(help_text='Name of the study; can be of any length', null=True),
        ),
        migrations.AddField(
            model_name='surveyarchive',
            name='name',
            field=models.TextField(help_text='Name of the study; can be of any length', null=True),
        ),
    ]