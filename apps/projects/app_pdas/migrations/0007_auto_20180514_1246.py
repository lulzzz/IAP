# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-05-14 04:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_pdas', '0006_auto_20180514_1245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factdemandtotal',
            name='dim_factory_id_original_unconstrained',
            field=models.ForeignKey(db_column='dim_factory_id_original_unconstrained', on_delete=django.db.models.deletion.DO_NOTHING, related_name='dim_factory_id_original_unconstrained', to='app_pdas.DimFactory'),
        ),
    ]
