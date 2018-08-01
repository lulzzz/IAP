# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-08-01 14:39
from __future__ import unicode_literals

import core.mixins_model
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_dms', '0014_auto_20180730_1246'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuyPlan',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('product_category', models.CharField(max_length=150, verbose_name='product category')),
                ('product_style', models.CharField(default='Style 1', max_length=150)),
                ('product_essential_trend', models.CharField(blank=True, max_length=100, null=True, verbose_name='essential trend')),
                ('product_basic_fashion', models.CharField(blank=True, max_length=100, null=True, verbose_name='basic fashion')),
                ('product_carryover', models.CharField(blank=True, max_length=100, null=True, verbose_name='carry over')),
                ('product_division', models.CharField(max_length=150, verbose_name='product group')),
                ('pricing_cost', models.IntegerField(blank=True, default=0, null=True, verbose_name='cost')),
                ('pricing_selling_price', models.IntegerField(blank=True, default=0, null=True, verbose_name='selling price')),
                ('range_width_style_colour_py', models.IntegerField(blank=True, default=0, null=True, verbose_name='# of style-colour codes PY')),
                ('line_life_in_weeks', models.IntegerField(blank=True, default=0, null=True)),
                ('rate_of_sales', models.FloatField(blank=True, default=0, null=True)),
                ('number_of_stores', models.IntegerField(blank=True, default=0, null=True)),
                ('targeted_sell_thru', models.IntegerField(blank=True, default=0, null=True, verbose_name='targeted sell thru %')),
                ('quantity_to_buy', models.IntegerField(blank=True, default=0, null=True)),
                ('otc_quantity', models.IntegerField(blank=True, default=0, null=True, verbose_name='OTB quantity')),
                ('range_effectiveness_style_colour_py', models.IntegerField(blank=True, default=0, null=True, verbose_name='range effectiveness')),
                ('size_curve_xs', models.IntegerField(blank=True, default=0, null=True, verbose_name='size curve XS (10%)')),
                ('size_curve_s', models.IntegerField(blank=True, default=0, null=True, verbose_name='size curve S (20%)')),
                ('size_curve_m', models.IntegerField(blank=True, default=0, null=True, verbose_name='size curve M (30%)')),
                ('size_curve_l', models.IntegerField(blank=True, default=0, null=True, verbose_name='size curve L (30%)')),
                ('size_curve_xl', models.IntegerField(blank=True, default=0, null=True, verbose_name='size curve XL (10%)')),
                ('dim_iapfilter', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app_dms.DimIAPFilter')),
            ],
            bases=(models.Model, core.mixins_model.ModelFormFieldNames),
        ),
        migrations.AlterModelOptions(
            name='dimiapcycle',
            options={'verbose_name': 'IAP Cycle'},
        ),
        migrations.AlterField(
            model_name='dimiapcycle',
            name='completion_dt',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Completion Date'),
        ),
        migrations.AlterField(
            model_name='dimiapcycle',
            name='dim_iapfilter',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app_dms.DimIAPFilter', verbose_name='IAP Filter'),
        ),
        migrations.AlterField(
            model_name='dimiapcycle',
            name='dim_iapstep',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_dms.DimIAPStep', verbose_name='IAP Step'),
        ),
        migrations.AlterField(
            model_name='dimiapcycle',
            name='is_completed',
            field=models.BooleanField(default=False, verbose_name='Status'),
        ),
        migrations.AlterUniqueTogether(
            name='buyplan',
            unique_together=set([('dim_iapfilter', 'product_category', 'product_style', 'product_essential_trend', 'product_basic_fashion')]),
        ),
    ]
