# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-05-14 04:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_pdas', '0005_auto_20180514_1245'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='factdemandtotal',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='factdemandtotal',
            name='quantity_unconsumed',
        ),
    ]
