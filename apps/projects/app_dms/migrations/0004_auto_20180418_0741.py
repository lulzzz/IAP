# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-04-17 23:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_dms', '0003_planbystore_country'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='IAPCycle',
            new_name='DimIAPCycle',
        ),
    ]
