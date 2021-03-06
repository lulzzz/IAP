# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-08-26 04:41
from __future__ import unicode_literals

import core.mixins_model
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_dms', '0021_auto_20180826_1206'),
    ]

    operations = [
        migrations.CreateModel(
            name='OTBPlanSupport',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('region', models.CharField(max_length=45)),
                ('net_sales', models.IntegerField(default=0)),
                ('trade_product_sales', models.IntegerField(default=0)),
                ('total_sales', models.IntegerField(default=0)),
                ('average_vat_percentage', models.FloatField(default=0)),
                ('average_vat', models.IntegerField(default=0, verbose_name='average VAT')),
                ('gross_sales', models.IntegerField(default=0)),
                ('dim_iapfilter', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app_dms.DimIAPFilter')),
            ],
            bases=(models.Model, core.mixins_model.ModelFormFieldNames),
        ),
        migrations.AlterUniqueTogether(
            name='otbplansupport',
            unique_together=set([('dim_iapfilter', 'region')]),
        ),
    ]
