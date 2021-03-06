# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-04-09 00:17
from __future__ import unicode_literals

import core.mixins_model
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DimChannel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Channel',
            },
            bases=(models.Model, core.mixins_model.ModelFormFieldNames),
        ),
        migrations.CreateModel(
            name='DimDate',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('full_date', models.DateField()),
                ('year_month_name', models.CharField(max_length=7)),
                ('sales_season', models.CharField(max_length=2)),
                ('sales_year', models.IntegerField()),
                ('sales_cw', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='DimIAPFilter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sales_year', models.IntegerField()),
                ('sales_season', models.CharField(max_length=2)),
                ('dim_channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_dms.DimChannel')),
            ],
            options={
                'verbose_name': 'IAP Filter',
            },
            bases=(models.Model, core.mixins_model.ModelFormFieldNames),
        ),
        migrations.CreateModel(
            name='DimIAPStep',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('position', models.PositiveIntegerField(unique=True)),
            ],
            options={
                'verbose_name': 'IAP Step',
            },
            bases=(models.Model, core.mixins_model.ModelFormFieldNames),
        ),
        migrations.CreateModel(
            name='DimLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(max_length=45)),
                ('country', models.CharField(max_length=100, unique=True)),
                ('country_code_a2', models.CharField(max_length=2, unique=True, validators=[django.core.validators.RegexValidator(code='nomatch', message='Length must be 2', regex='^.{2}$')], verbose_name='country code A2')),
                ('country_code_a3', models.CharField(max_length=3, unique=True, validators=[django.core.validators.RegexValidator(code='nomatch', message='Length must be 3', regex='^.{3}$')], verbose_name='country code A3')),
            ],
            options={
                'verbose_name': 'Location',
            },
            bases=(models.Model, core.mixins_model.ModelFormFieldNames),
        ),
        migrations.CreateModel(
            name='DimProduct',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('productcode', models.CharField(max_length=100, unique=True, verbose_name='product code')),
                ('productshortdescription', models.CharField(blank=True, max_length=100, null=True, verbose_name='short description')),
                ('productdescription', models.CharField(blank=True, max_length=100, null=True, verbose_name='description')),
                ('size', models.CharField(blank=True, max_length=100, null=True)),
                ('colour', models.CharField(blank=True, max_length=100, null=True)),
                ('style', models.CharField(blank=True, max_length=500, null=True)),
                ('category', models.CharField(blank=True, max_length=500, null=True)),
                ('division', models.CharField(blank=True, max_length=500, null=True)),
                ('essential_trend', models.CharField(blank=True, max_length=100, null=True)),
                ('basic_fashion', models.CharField(blank=True, max_length=100, null=True)),
                ('quality', models.IntegerField(blank=True, null=True)),
                ('image', models.CharField(blank=True, max_length=500, null=True)),
            ],
            bases=(models.Model, core.mixins_model.ModelFormFieldNames),
        ),
        migrations.CreateModel(
            name='DimStore',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('store_code', models.CharField(max_length=100, unique=True)),
                ('store_name', models.CharField(blank=True, max_length=500, null=True)),
                ('store_display_label', models.CharField(blank=True, max_length=500, null=True)),
                ('iln', models.CharField(blank=True, max_length=100, null=True, verbose_name='ILN')),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('region_tax_rate', models.CharField(blank=True, max_length=100, null=True)),
                ('local_currency', models.CharField(blank=True, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('store_type', models.CharField(blank=True, max_length=100, null=True)),
                ('store_location', models.CharField(blank=True, max_length=100, null=True)),
                ('store_style', models.CharField(blank=True, max_length=100, null=True)),
                ('customer_type', models.CharField(blank=True, max_length=100, null=True)),
                ('potential', models.CharField(blank=True, max_length=100, null=True)),
                ('store_size', models.FloatField(blank=True, null=True)),
                ('store_tier', models.IntegerField(blank=True, null=True)),
                ('dim_channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_dms.DimChannel', verbose_name='channel')),
                ('dim_location', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app_dms.DimLocation', verbose_name='country code A2')),
            ],
            options={
                'verbose_name': 'Store',
            },
            bases=(models.Model, core.mixins_model.ModelFormFieldNames),
        ),
        migrations.CreateModel(
            name='FactInventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inventorydate', models.DateField()),
                ('unitonhand', models.IntegerField(blank=True, null=True)),
                ('unitonorder', models.FloatField(blank=True, null=True)),
                ('unitrequired', models.FloatField(blank=True, null=True)),
                ('unitallocated', models.FloatField(blank=True, null=True)),
                ('leadtime', models.FloatField(blank=True, null=True)),
                ('unitprice', models.FloatField(blank=True, null=True)),
                ('salesprice', models.FloatField(blank=True, null=True)),
                ('minimumstocklevel', models.FloatField(blank=True, null=True)),
                ('reorderlevel', models.FloatField(blank=True, null=True)),
                ('excludedlevel', models.FloatField(blank=True, null=True)),
                ('orderamount', models.FloatField(blank=True, null=True)),
                ('orderlock', models.FloatField(blank=True, null=True)),
                ('packsize', models.FloatField(blank=True, null=True)),
                ('minimumorderquantity', models.FloatField(blank=True, null=True)),
                ('safetylevel', models.FloatField(blank=True, null=True)),
                ('totalsales', models.FloatField(blank=True, null=True)),
                ('numbersales', models.FloatField(blank=True, null=True)),
                ('paretostore', models.CharField(blank=True, max_length=500, null=True)),
                ('paretoglobal', models.CharField(blank=True, max_length=500, null=True)),
                ('replenishcode', models.CharField(blank=True, max_length=500, null=True)),
                ('dcavailable', models.FloatField(blank=True, null=True)),
                ('createdate', models.DateTimeField(blank=True, null=True)),
                ('source', models.CharField(blank=True, max_length=500, null=True)),
                ('supplierproductcode', models.FloatField(blank=True, null=True)),
                ('productid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_dms.DimProduct')),
                ('storeid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_dms.DimStore')),
            ],
        ),
        migrations.CreateModel(
            name='FactMovements',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movementid', models.CharField(blank=True, max_length=100, null=True)),
                ('movementdate', models.DateField()),
                ('movementtype', models.CharField(blank=True, max_length=1, null=True)),
                ('units', models.IntegerField(blank=True, null=True)),
                ('costvalue', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('salesvalue', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('movementnumber', models.CharField(blank=True, max_length=100, null=True)),
                ('movementline', models.IntegerField(blank=True, null=True)),
                ('insertdate', models.DateTimeField(blank=True, null=True)),
                ('updatedate', models.DateTimeField(blank=True, null=True)),
                ('insertsource', models.CharField(blank=True, max_length=20, null=True)),
                ('updatesource', models.CharField(blank=True, max_length=20, null=True)),
                ('dim_date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_dms.DimDate')),
                ('dim_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_dms.DimProduct')),
                ('dim_store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_dms.DimStore')),
            ],
        ),
        migrations.CreateModel(
            name='FactSalesForecast',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('units', models.IntegerField(blank=True, null=True)),
                ('fitted', models.IntegerField(blank=True, null=True)),
                ('rmse', models.IntegerField(blank=True, null=True)),
                ('overwritten', models.IntegerField(blank=True, null=True)),
                ('user_name', models.CharField(blank=True, max_length=100, null=True)),
                ('is_locked', models.IntegerField(blank=True, null=True)),
                ('dim_date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_dms.DimDate')),
                ('dim_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_dms.DimProduct')),
                ('dim_store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_dms.DimStore')),
            ],
        ),
        migrations.CreateModel(
            name='FeatureImportanceOutputSimulation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('features', models.CharField(max_length=250)),
                ('importance', models.FloatField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FeatureProductInput',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('units', models.IntegerField(blank=True, null=True)),
                ('salesvalueeur', models.FloatField(blank=True, null=True, verbose_name='sales value (EUR)')),
                ('cluster_ai', models.CharField(max_length=2, verbose_name='cluster AI')),
                ('cluster_user', models.CharField(max_length=2)),
                ('dim_iapfilter', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app_dms.DimIAPFilter')),
                ('dim_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_dms.DimProduct')),
                ('dim_store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_dms.DimStore')),
            ],
            bases=(models.Model, core.mixins_model.ModelFormFieldNames),
        ),
        migrations.CreateModel(
            name='FeatureProductInputByCluster',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cluster', models.CharField(max_length=2)),
                ('units', models.IntegerField(blank=True, null=True)),
                ('salesvalueeur', models.FloatField(blank=True, null=True, verbose_name='sales value (EUR)')),
                ('dim_iapfilter', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app_dms.DimIAPFilter')),
                ('dim_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_dms.DimProduct')),
            ],
            bases=(models.Model, core.mixins_model.ModelFormFieldNames),
        ),
        migrations.CreateModel(
            name='FeatureProductOutputSimulation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cluster_ai', models.CharField(max_length=2, verbose_name='cluster AI')),
                ('cluster_user', models.CharField(max_length=2)),
                ('units', models.IntegerField(blank=True, null=True)),
                ('dim_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_dms.DimProduct')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FeatureStoreInput',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('net_retail_sales_in_eur_ty', models.FloatField(blank=True, null=True, verbose_name='net sales TY')),
                ('average_monthly_sales_for_ty', models.FloatField(blank=True, null=True, verbose_name='average monthly sales TY')),
                ('sku_count', models.IntegerField(blank=True, null=True, verbose_name='SKU count')),
                ('relative_sales_volume_ty', models.FloatField(blank=True, null=True, verbose_name='relative sales TY')),
                ('average_value_transaction', models.FloatField(blank=True, null=True, verbose_name='AVT')),
                ('sales_swimwear', models.FloatField(blank=True, null=True)),
                ('sales_lingerie', models.FloatField(blank=True, null=True)),
                ('sales_legwear', models.FloatField(blank=True, null=True)),
                ('sales_ready_to_wear', models.FloatField(blank=True, null=True)),
                ('sales_adv_promotion', models.FloatField(blank=True, null=True, verbose_name='sales ADV promotion')),
                ('sales_accessories', models.FloatField(blank=True, null=True)),
                ('cluster_ai', models.CharField(max_length=2, verbose_name='cluster AI')),
                ('cluster_user', models.CharField(max_length=2)),
                ('optimal_assortment_similarity_coefficient', models.FloatField(blank=True, null=True)),
                ('dim_iapfilter', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app_dms.DimIAPFilter')),
                ('dim_store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_dms.DimStore', verbose_name='store code')),
            ],
            bases=(models.Model, core.mixins_model.ModelFormFieldNames),
        ),
        migrations.CreateModel(
            name='FeatureStoreOutputSimulation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cluster_ai', models.CharField(max_length=2, verbose_name='cluster AI')),
                ('cluster_user', models.CharField(max_length=2)),
                ('master_assortment_similarity_coefficient', models.FloatField(blank=True, null=True)),
                ('feature', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app_dms.FeatureStoreInput')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='IAPCycle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_completed', models.BooleanField(default=False)),
                ('completion_dt', models.DateTimeField(blank=True, null=True)),
                ('dim_iapfilter', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app_dms.DimIAPFilter')),
                ('dim_iapstep', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_dms.DimIAPStep')),
            ],
        ),
        migrations.CreateModel(
            name='KPI',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salesdate', models.DateTimeField(blank=True, null=True)),
                ('salescomp', models.IntegerField(blank=True, null=True)),
                ('locationcode', models.IntegerField(blank=True, null=True)),
                ('salesunits', models.IntegerField(blank=True, null=True)),
                ('netretailsaleslocal', models.BigIntegerField(blank=True, null=True)),
                ('netretailsaleseur', models.BigIntegerField(blank=True, null=True)),
                ('currency', models.CharField(blank=True, max_length=500, null=True)),
                ('transactions', models.IntegerField(blank=True, null=True)),
                ('upt', models.IntegerField(blank=True, null=True)),
                ('avtlocal', models.IntegerField(blank=True, null=True)),
                ('avteur', models.IntegerField(blank=True, null=True)),
                ('ppplocal', models.FloatField(blank=True, null=True)),
                ('pppeur', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlanByMonth',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('year_month_name_ly', models.CharField(max_length=7, verbose_name='month LY')),
                ('unit_sales_ly', models.IntegerField(blank=True, null=True, verbose_name='unit sales LY')),
                ('value_sales_ly', models.FloatField(blank=True, null=True, verbose_name='value sales LY')),
                ('year_month_name_py', models.CharField(max_length=7, verbose_name='month PY')),
                ('unit_sales_py_product_category_level', models.IntegerField(blank=True, default=0, null=True, verbose_name='unit sales PY brand')),
                ('value_sales_py_product_category_level', models.FloatField(blank=True, default=0, null=True, verbose_name='value sales PY brand')),
                ('unit_sales_py_store_level', models.IntegerField(blank=True, default=0, null=True, verbose_name='unit sales PY retail')),
                ('value_sales_py_store_level', models.FloatField(blank=True, default=0, null=True, verbose_name='value sales PY retail')),
                ('unit_sales_py_year_month_level', models.IntegerField(blank=True, default=0, null=True, verbose_name='units')),
                ('value_sales_py_year_month_level', models.FloatField(blank=True, default=0, null=True, verbose_name='sales value')),
                ('dim_iapfilter', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app_dms.DimIAPFilter')),
            ],
            bases=(models.Model, core.mixins_model.ModelFormFieldNames),
        ),
        migrations.CreateModel(
            name='PlanByMonthProductCategoryStore',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('year_month_name_ly', models.CharField(max_length=7, verbose_name='month LY')),
                ('product_category', models.CharField(max_length=150, verbose_name='product category')),
                ('cluster_user', models.CharField(max_length=2)),
                ('product_division', models.CharField(max_length=150, verbose_name='product group')),
                ('unit_sales_py', models.IntegerField(blank=True, null=True, verbose_name='unit sales PY')),
                ('value_sales_py', models.FloatField(blank=True, null=True, verbose_name='value sales PY')),
                ('dim_iapfilter', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app_dms.DimIAPFilter')),
                ('dim_store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_dms.DimStore')),
            ],
        ),
        migrations.CreateModel(
            name='PlanByProductCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('product_category', models.CharField(max_length=150, verbose_name='product category')),
                ('product_division', models.CharField(max_length=150, verbose_name='product group')),
                ('unit_sales_ly', models.IntegerField(blank=True, null=True, verbose_name='unit sales LY')),
                ('value_sales_ly', models.FloatField(blank=True, null=True, verbose_name='value sales LY')),
                ('unit_sales_py_index', models.FloatField(blank=True, null=True, verbose_name='index')),
                ('unit_sales_py_mix', models.FloatField(blank=True, null=True, verbose_name='mix')),
                ('unit_sales_py', models.IntegerField(blank=True, null=True, verbose_name='unit sales PY')),
                ('value_sales_py', models.FloatField(blank=True, null=True, verbose_name='value sales PY')),
                ('dim_iapfilter', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app_dms.DimIAPFilter')),
            ],
            bases=(models.Model, core.mixins_model.ModelFormFieldNames),
        ),
        migrations.CreateModel(
            name='PlanByStore',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('store_code', models.CharField(max_length=100, unique=True)),
                ('store_name', models.CharField(blank=True, max_length=500, null=True)),
                ('cluster_user', models.CharField(max_length=2)),
                ('unit_sales_ly', models.IntegerField(blank=True, null=True, verbose_name='unit sales LY')),
                ('value_sales_ly', models.FloatField(blank=True, null=True, verbose_name='value sales LY')),
                ('unit_sales_py_index', models.FloatField(blank=True, null=True, verbose_name='index')),
                ('unit_sales_py_mix', models.FloatField(blank=True, null=True, verbose_name='mix')),
                ('unit_sales_py', models.IntegerField(blank=True, null=True, verbose_name='unit sales PY')),
                ('value_sales_py', models.FloatField(blank=True, null=True, verbose_name='value sales PY')),
                ('dim_iapfilter', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app_dms.DimIAPFilter')),
            ],
            bases=(models.Model, core.mixins_model.ModelFormFieldNames),
        ),
        migrations.CreateModel(
            name='RangeArchitecture',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('product_category', models.CharField(max_length=150, verbose_name='product category')),
                ('product_division', models.CharField(max_length=150, verbose_name='product group')),
                ('product_essential_trend', models.CharField(blank=True, max_length=100, null=True, verbose_name='essential trend')),
                ('product_basic_fashion', models.CharField(blank=True, max_length=100, null=True, verbose_name='basic fashion')),
                ('range_depth_ly', models.IntegerField(blank=True, null=True, verbose_name='range depth style level LY')),
                ('range_width_style_ly', models.IntegerField(blank=True, null=True, verbose_name='range width style level LY')),
                ('range_width_style_colour_ly', models.IntegerField(blank=True, null=True, verbose_name='range width style-colour level LY')),
                ('range_depth_py', models.IntegerField(blank=True, null=True, verbose_name='range depth style level PY')),
                ('range_width_style_py', models.FloatField(blank=True, null=True, verbose_name='range width style level PY')),
                ('dim_iapfilter', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app_dms.DimIAPFilter')),
            ],
            bases=(models.Model, core.mixins_model.ModelFormFieldNames),
        ),
        migrations.CreateModel(
            name='RangeMaster',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('model_number', models.CharField(max_length=100)),
                ('style_number', models.CharField(max_length=100)),
                ('colour_number', models.CharField(max_length=100)),
                ('product_division', models.CharField(max_length=150, verbose_name='product group')),
                ('product_category', models.CharField(max_length=150, verbose_name='product category')),
                ('product_essential_trend', models.CharField(blank=True, max_length=100, null=True, verbose_name='essential trend')),
                ('product_basic_fashion', models.CharField(blank=True, max_length=100, null=True, verbose_name='basic fashion')),
                ('model_name', models.CharField(max_length=100)),
                ('style_name', models.CharField(blank=True, max_length=100, null=True)),
                ('colour_name', models.CharField(blank=True, max_length=100, null=True)),
                ('material', models.CharField(blank=True, max_length=100, null=True)),
                ('dim_iapfilter', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app_dms.DimIAPFilter')),
            ],
            bases=(models.Model, core.mixins_model.ModelFormFieldNames),
        ),
        migrations.CreateModel(
            name='StrategicSalesPlan',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sales_year', models.IntegerField(default=2017)),
                ('sales_season', models.CharField(default='SS', max_length=2)),
                ('region', models.CharField(max_length=45)),
                ('scenario', models.CharField(default='conservative', max_length=45)),
                ('gross_sales_index', models.FloatField(blank=True, null=True)),
                ('gross_sales', models.FloatField(blank=True, null=True)),
                ('avt', models.FloatField(blank=True, null=True)),
                ('gross_sales_per_unit', models.IntegerField(blank=True, null=True)),
                ('discounts', models.FloatField(blank=True, null=True)),
                ('returns', models.FloatField(blank=True, null=True)),
                ('net_sales', models.FloatField(blank=True, null=True)),
                ('sell_through_ratio', models.FloatField(blank=True, null=True)),
                ('sell_in', models.FloatField(blank=True, null=True)),
                ('markup', models.FloatField(blank=True, null=True)),
                ('gross_margin_percentage', models.FloatField(blank=True, null=True)),
                ('gross_margin', models.FloatField(blank=True, null=True)),
                ('buying_budget', models.FloatField(blank=True, null=True)),
                ('gmroi_percentage_target', models.FloatField(blank=True, null=True)),
                ('beginning_season_inventory', models.FloatField(blank=True, null=True)),
                ('ending_season_inventory', models.FloatField(blank=True, null=True)),
                ('markdown', models.FloatField(blank=True, null=True)),
                ('row_styling', models.CharField(blank=True, max_length=45, null=True)),
                ('dim_channel', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app_dms.DimChannel')),
            ],
            bases=(models.Model, core.mixins_model.ModelFormFieldNames),
        ),
        migrations.AlterUniqueTogether(
            name='strategicsalesplan',
            unique_together=set([('dim_channel', 'sales_year', 'sales_season', 'region', 'scenario')]),
        ),
        migrations.AlterUniqueTogether(
            name='rangemaster',
            unique_together=set([('dim_iapfilter', 'model_number', 'style_number', 'colour_number')]),
        ),
        migrations.AlterUniqueTogether(
            name='rangearchitecture',
            unique_together=set([('dim_iapfilter', 'product_category')]),
        ),
        migrations.AlterUniqueTogether(
            name='planbystore',
            unique_together=set([('dim_iapfilter', 'store_code')]),
        ),
        migrations.AlterUniqueTogether(
            name='planbyproductcategory',
            unique_together=set([('dim_iapfilter', 'product_category')]),
        ),
        migrations.AlterUniqueTogether(
            name='planbymonthproductcategorystore',
            unique_together=set([('dim_iapfilter', 'year_month_name_ly', 'dim_store', 'product_category')]),
        ),
        migrations.AlterUniqueTogether(
            name='planbymonth',
            unique_together=set([('dim_iapfilter', 'year_month_name_ly')]),
        ),
        migrations.AlterUniqueTogether(
            name='iapcycle',
            unique_together=set([('dim_iapfilter', 'dim_iapstep')]),
        ),
        migrations.AlterUniqueTogether(
            name='featurestoreoutputsimulation',
            unique_together=set([('feature', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='featurestoreinput',
            unique_together=set([('dim_iapfilter', 'dim_store')]),
        ),
        migrations.AlterUniqueTogether(
            name='featureproductoutputsimulation',
            unique_together=set([('cluster_user', 'dim_product', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='featureproductinputbycluster',
            unique_together=set([('dim_iapfilter', 'cluster', 'dim_product')]),
        ),
        migrations.AlterUniqueTogether(
            name='featureproductinput',
            unique_together=set([('dim_iapfilter', 'dim_store', 'dim_product')]),
        ),
        migrations.AlterUniqueTogether(
            name='featureimportanceoutputsimulation',
            unique_together=set([('user', 'features')]),
        ),
        migrations.AlterUniqueTogether(
            name='factsalesforecast',
            unique_together=set([('dim_date', 'dim_store', 'dim_product')]),
        ),
    ]
