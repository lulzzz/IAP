# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-07-27 10:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_dms', '0009_auto_20180723_1948'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rangearchitecture',
            name='product_basic_fashion',
        ),
        migrations.RemoveField(
            model_name='rangearchitecture',
            name='product_essential_trend',
        ),
        migrations.RemoveField(
            model_name='rangearchitecture',
            name='range_depth_ly',
        ),
        migrations.RemoveField(
            model_name='rangearchitecture',
            name='range_depth_py',
        ),
        migrations.RemoveField(
            model_name='rangearchitecture',
            name='range_width_style_colour_ly',
        ),
        migrations.RemoveField(
            model_name='rangearchitecture',
            name='range_width_style_ly',
        ),
        migrations.RemoveField(
            model_name='rangearchitecture',
            name='range_width_style_py',
        ),
        migrations.AddField(
            model_name='rangearchitecture',
            name='range_effectiveness_ly_essential_basic',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='range effectiveness LY essential basic'),
        ),
        migrations.AddField(
            model_name='rangearchitecture',
            name='range_effectiveness_ly_essential_fashion',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='range effectiveness LY essential fashion'),
        ),
        migrations.AddField(
            model_name='rangearchitecture',
            name='range_effectiveness_ly_total',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='range effectiveness LY total'),
        ),
        migrations.AddField(
            model_name='rangearchitecture',
            name='range_effectiveness_ly_trend_basic',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='range effectiveness LY trend basic'),
        ),
        migrations.AddField(
            model_name='rangearchitecture',
            name='range_effectiveness_ly_trend_fashion',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='range effectiveness LY trend fashion'),
        ),
        migrations.AddField(
            model_name='rangearchitecture',
            name='range_effectiveness_py_carry_over',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='range effectiveness PY carry over'),
        ),
        migrations.AddField(
            model_name='rangearchitecture',
            name='range_effectiveness_py_essential_basic',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='range effectiveness PY essential basic'),
        ),
        migrations.AddField(
            model_name='rangearchitecture',
            name='range_effectiveness_py_essential_fashion',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='range effectiveness PY essential fashion'),
        ),
        migrations.AddField(
            model_name='rangearchitecture',
            name='range_effectiveness_py_total',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='range effectiveness PY total'),
        ),
        migrations.AddField(
            model_name='rangearchitecture',
            name='range_effectiveness_py_trend_basic',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='range effectiveness PY trend basic'),
        ),
        migrations.AddField(
            model_name='rangearchitecture',
            name='range_effectiveness_py_trend_fashion',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='range effectiveness PY trend fashion'),
        ),
        migrations.AddField(
            model_name='rangearchitecture',
            name='range_performance_ly',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='ASP LY'),
        ),
        migrations.AddField(
            model_name='rangearchitecture',
            name='range_performance_ty',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='ASP TY'),
        ),
        migrations.AddField(
            model_name='rangearchitecture',
            name='range_sales_ly_essential_basic',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='range sales LY essential basic'),
        ),
        migrations.AddField(
            model_name='rangearchitecture',
            name='range_sales_ly_essential_fashion',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='range sales LY essential fashion'),
        ),
        migrations.AddField(
            model_name='rangearchitecture',
            name='range_sales_ly_total',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='range sales LY total'),
        ),
        migrations.AddField(
            model_name='rangearchitecture',
            name='range_sales_ly_trend_basic',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='range sales LY trend basic'),
        ),
        migrations.AddField(
            model_name='rangearchitecture',
            name='range_sales_ly_trend_fashion',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='range sales LY trend fashion'),
        ),
        migrations.AddField(
            model_name='rangearchitecture',
            name='range_width_style_colour_ly_essential_basic',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='range width style-colour level LY essential basic'),
        ),
        migrations.AddField(
            model_name='rangearchitecture',
            name='range_width_style_colour_ly_essential_fashion',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='range width style-colour level LY essential fashion'),
        ),
        migrations.AddField(
            model_name='rangearchitecture',
            name='range_width_style_colour_ly_total',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='style-colour count LY'),
        ),
        migrations.AddField(
            model_name='rangearchitecture',
            name='range_width_style_colour_ly_trend_basic',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='range width style-colour level LY trend basic'),
        ),
        migrations.AddField(
            model_name='rangearchitecture',
            name='range_width_style_colour_ly_trend_fashion',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='range width style-colour level LY trend fashion'),
        ),
        migrations.AddField(
            model_name='rangearchitecture',
            name='range_width_style_colour_py_carry_over',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='range width style-colour level PY carry over'),
        ),
        migrations.AddField(
            model_name='rangearchitecture',
            name='range_width_style_colour_py_essential_basic',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='range width style-colour level PY essential basic'),
        ),
        migrations.AddField(
            model_name='rangearchitecture',
            name='range_width_style_colour_py_essential_fashion',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='range width style-colour level PY essential fashion'),
        ),
        migrations.AddField(
            model_name='rangearchitecture',
            name='range_width_style_colour_py_total',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='style-colour count PY'),
        ),
        migrations.AddField(
            model_name='rangearchitecture',
            name='range_width_style_colour_py_trend_basic',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='range width style-colour level PY trend basic'),
        ),
        migrations.AddField(
            model_name='rangearchitecture',
            name='range_width_style_colour_py_trend_fashion',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='range width style-colour level PY trend fashion'),
        ),
        migrations.AddField(
            model_name='rangearchitecture',
            name='range_width_style_ly_essential_basic',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='range width style level LY essential basic'),
        ),
        migrations.AddField(
            model_name='rangearchitecture',
            name='range_width_style_ly_essential_basic_avg_colour_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='rangearchitecture',
            name='range_width_style_ly_essential_fashion',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='range width style level LY essential fashion'),
        ),
        migrations.AddField(
            model_name='rangearchitecture',
            name='range_width_style_ly_essential_fashion_avg_colour_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='rangearchitecture',
            name='range_width_style_ly_total',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='style count LY'),
        ),
        migrations.AddField(
            model_name='rangearchitecture',
            name='range_width_style_ly_trend_basic',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='range width style level LY trend basic'),
        ),
        migrations.AddField(
            model_name='rangearchitecture',
            name='range_width_style_ly_trend_basic_avg_colour_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='rangearchitecture',
            name='range_width_style_ly_trend_fashion',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='range width style level LY trend fashion'),
        ),
        migrations.AddField(
            model_name='rangearchitecture',
            name='range_width_style_ly_trend_fashion_avg_colour_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='rangearchitecture',
            name='range_width_style_py_carry_over',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='range width style level PY carry over'),
        ),
        migrations.AddField(
            model_name='rangearchitecture',
            name='range_width_style_py_essential_basic',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='range width style level PY essential basic'),
        ),
        migrations.AddField(
            model_name='rangearchitecture',
            name='range_width_style_py_essential_fashion',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='range width style level PY essential fashion'),
        ),
        migrations.AddField(
            model_name='rangearchitecture',
            name='range_width_style_py_total',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='style count PY'),
        ),
        migrations.AddField(
            model_name='rangearchitecture',
            name='range_width_style_py_trend_basic',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='range width style level PY trend basic'),
        ),
        migrations.AddField(
            model_name='rangearchitecture',
            name='range_width_style_py_trend_fashion',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='range width style level PY trend fashion'),
        ),
    ]
