# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-17 06:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_console', '0006_auto_20171215_1501'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='duration',
            field=models.IntegerField(blank=True, help_text='in seconds', null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='schema',
            field=models.CharField(blank=True, default='dbo', max_length=100, null=True),
        ),
    ]
