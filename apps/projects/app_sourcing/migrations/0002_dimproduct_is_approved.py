# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-03-22 15:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_sourcing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dimproduct',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]
