# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-07-23 11:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_dms', '0008_auto_20180723_1726'),
    ]

    operations = [
        migrations.AddField(
            model_name='strategicsalesplan',
            name='channel_mix',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='strategicsalesplan',
            name='seasonal_mix',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
