# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-06-12 07:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_pipeline', '0003_auto_20180530_1206'),
    ]

    operations = [
        migrations.CreateModel(
            name='MetadataPK',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_name', models.CharField(max_length=500)),
                ('metadata', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_pipeline.Metadata')),
            ],
        ),
        migrations.CreateModel(
            name='MetadataRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField()),
                ('metadata', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_pipeline.Metadata')),
            ],
        ),
    ]
