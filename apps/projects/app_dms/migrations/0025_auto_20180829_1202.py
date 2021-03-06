# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-08-29 04:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_dms', '0024_otbplanmix_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='otbplanmix',
            name='product_type',
            field=models.CharField(default=1, max_length=100, verbose_name='product type'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='otbplanmix',
            unique_together=set([('dim_iapfilter', 'region', 'product_type')]),
        ),
    ]
