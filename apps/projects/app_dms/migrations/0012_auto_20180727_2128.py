# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-07-27 13:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_dms', '0011_auto_20180727_2111'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rangearchitecture',
            name='range_performance_ty',
        ),
        migrations.AddField(
            model_name='rangearchitecture',
            name='range_performance_py',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='ASP PY'),
        ),
    ]
