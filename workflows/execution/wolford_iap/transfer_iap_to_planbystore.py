import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(sys.path[0]))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.projects.settings_wolford_iap.project")

import django
django.setup()

from django.conf import settings
from apps.projects.app_dms import models

from workflows.remote_procedure.wolford_iap.calls_iap import insert_update


# General rules
input_select = [
    {
        'function': '',
        'table': 'app_dms_dimdate',
        'column': 'year_month_name',
        'new_name': ''
    },
    {
        'function': 'sum',
        'table': 'app_dms_factmovements',
        'column': 'units',
        'new_name': 'u'
    },
    {
        'function': 'sum',
        'table': 'app_dms_factmovements',
        'column': 'salesvalue',
        'new_name': 'v'
    }
]

input_from = ['app_dms_factmovements']

input_join = [
    {
        'join_method': 'inner',
        'left_table': 'app_dms_factmovements',
        'right_table': 'app_dms_dimdate',
        'left_key_0': 'dim_date_id',
        'right_key_0': 'id'
    },
    {
        'join_method': 'inner',
        'left_table': 'app_dms_factmovements',
        'right_table': 'app_dms_dimstore',
        'left_key_0': 'dim_store_id',
        'right_key_0': 'id'
    },
]

input_groupby = [
    {
        'table': 'app_dms_dimdate',
        'column': 'year_month_name'
    },
    {
        'table': 'app_dms_dimdate',
        'column': 'year_month_name'
    },
]

input_update_condition = [
    {
        'table': 'app_dms_planbymonth',
        'column': 'year_month_name_ly',
        'operator': 'equal',
        'value_table': 'tailormade_table',
        'value_column': 'year_month_name',
        'value_value': ''
    },
]

input_update = {
    'unit_sales_ly': 'u',
    'value_sales_ly': 'v',
    'year_month_name_ly': 'year_month_name',
    'year_month_name_py': 'year_month_name',
    'unit_sales_py_year_month_level': 'u',
    'value_sales_py_year_month_level': 'v',
}


# Specific rules
queryset = models.DimIAPFilter.objects.all().order_by('id')
for item in queryset:
    dim_iapfilter_id = item.id
    dim_channel_id = item.dim_channel_id
    sales_year = item.sales_year
    sales_season = item.sales_season

    input_where = [
        {
            'table': 'app_dms_dimstore',
            'column': 'dim_channel_id',
            'operator': 'equal',
            'value': dim_channel_id
        },
        {
            'table': 'app_dms_dimdate',
            'column': 'sales_year',
            'operator': 'equal',
            'value': sales_year
        },
        {
            'table': 'app_dms_dimdate',
            'column': 'sales_season',
            'operator': 'equal',
            'value': sales_season
        },
    ]

    input_insert = {
        'dim_iapfilter_id': dim_iapfilter_id,
    }

    big_input = {
        'input_select': input_select,
        'input_from': input_from,
        'input_join': input_join,
        'input_where': input_where,
        'input_groupby': input_groupby,
        'input_update_condition': input_update_condition,
        'input_update': input_update,
        'input_insert': input_insert,
    }

    insert_update(**big_input)
