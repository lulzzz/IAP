import os
from datetime import datetime, timedelta

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.conf import settings as cp
from django.urls import reverse_lazy

from rest_framework import status # To return status codes
from rest_framework.views import APIView
from django.http import JsonResponse
from django.utils import timezone

from django.db.models import Count, Sum, Min, Max, Q
from django.db.models.functions import Lower, Upper

from blocks import views
from core import utils
from core import mixins_view
from apps.standards.app_console import mixins_apiview

from apps.standards.app_console import mixins_apiview
from apps.standards.app_console.models import UserPermissions
from apps.standards.app_console.models import GroupPermissions
from apps.standards.app_console.models import Item

from . import models
from . import forms
from . import serializers
from . import mixins_view as project_mixins_view

from workflows.core.hierarchy_utils import update_mix_index, convert_percentage
from workflows.execution.wolford_iap import calls

r"""
Master tables
"""
class MasterTableAPI(mixins_apiview.MasterTableAPIMixin):
    r"""
    View that updates master the master table specified in the request.
    Assuming user group has required permissions.
    """

    def get_model_obj(self):
        return eval('models.' + self.model_name)

    def get_serializer_obj(self):
        return eval('serializers.' + self.model_name + 'Serializer')


class MasterTableHeaderAPI(mixins_apiview.MasterTableHeaderAPIMixin):
    r"""
    View that loads the table header
    Assuming user group has required permissions.
    """

    def get_model_obj(self):
        return eval('models.' + self.model_name)

    def get_serializer_obj(self):
        return eval('serializers.' + self.model_name + 'Serializer')


r"""
Search
"""
class SearchAPI(APIView):
    r"""
    API controlling the intelligent search
    """

    def get(self, request, format=None, **kwargs):
        # Prepare result serializer
        serializer_combined = list()

        # Try getting parameter from URL
        query = self.kwargs.get('query', None)

        # Get parameter from GET
        if query is None:
            query = request.GET.get('term', '').replace('+', ' ')

        query_list_of_dict = [
            {
                'search_tab': 'search_tab_one_product', # only for multiple
                'model': models.DimProduct,
                'search_field_label': 'product code',
                'search_field': 'productcode',
                'search_type': 'icontains',
                'is_unique': True,
            },
            {
                'search_tab': 'search_tab_multiple_product', # only for multiple
                'model': models.DimProduct,
                'search_field_label': 'style',
                'search_field': 'style',
                'search_type': 'icontains',
                'is_unique': False,
            },
            {
                'search_tab': 'search_tab_multiple_product', # only for multiple
                'model': models.DimProduct,
                'search_field_label': 'colour',
                'search_field': 'colour',
                'search_type': 'icontains',
                'is_unique': False,
            },
            {
                'search_tab': 'search_tab_multiple_product', # only for multiple
                'model': models.DimProduct,
                'search_field_label': 'category',
                'search_field': 'category',
                'search_type': 'icontains',
                'is_unique': False,
            },
            {
                'search_tab': 'search_tab_multiple_product', # only for multiple
                'model': models.DimProduct,
                'search_field_label': 'division',
                'search_field': 'division',
                'search_type': 'icontains',
                'is_unique': False,
            },
            {
                'search_tab': 'search_tab_multiple_product', # only for multiple
                'model': models.DimProduct,
                'search_field_label': 'description',
                'search_field': 'productdescription',
                'search_type': 'icontains',
                'is_unique': False,
            },
            {
                'search_tab': 'search_tab_one_store', # only for multiple
                'model': models.DimStore,
                'search_field_label': 'store code',
                'search_field': 'store_code',
                'search_type': 'icontains',
                'is_unique': True,
            },
            {
                'search_tab': 'search_tab_one_store', # only for multiple
                'model': models.DimStore,
                'search_field_label': 'store name',
                'search_field': 'store_name',
                'search_type': 'icontains',
                'is_unique': True,
            },
            {
                'search_tab': 'search_tab_one_store', # only for multiple
                'model': models.DimStore,
                'search_field_label': 'store label',
                'search_field': 'store_display_label',
                'search_type': 'icontains',
                'is_unique': True,
            },
            {
                'search_tab': 'search_tab_multiple_store', # only for multiple
                'model': models.DimLocation,
                'search_field_label': 'store country',
                'search_field': 'country',
                'search_type': 'icontains',
                'is_unique': False,
            },
            {
                'search_tab': 'search_tab_multiple_store', # only for multiple
                'model': models.DimChannel,
                'search_field_label': 'store channel',
                'search_field': 'name',
                'search_type': 'icontains',
                'is_unique': False,
            },
        ]
        serializer_combined = utils.generate_search_list(query, query_list_of_dict)

        return JsonResponse(serializer_combined, safe=False)


class ProductAttributeTable(views.FormValidation):
    r"""
    View that shows/updates the product table
    """
    # Define variables
    # template_name = 'blocks/form_validation_django_as_p.html'
    form_class = forms.ProductForm
    model = models.DimProduct


class ProductImageGallery(views.MediaGallery):
    r"""
    View that shows the image from the retailisation website
    """

    def get_context_dict(self, request):
        pk = self.kwargs.get('pk', 0)
        model = get_object_or_404(models.DimProduct, pk=pk)

        return [
            {
                'url': model.image,
                'label': model.productcode,
                'full_row': True,
            }
        ]


class SalesForecastAPI(views.ChartAPI):
    r'''
    View that shows the sales volume details (meant for charts)
    '''
    model = models.FactMovements
    order_by = 'dim_date__year_month_name'
    xaxis = 'dim_date__year_month_name'
    chart_label = 'Sales'
    aggregation = 'units'
    filter_dict = None

    # Overwrite variables
    def __init__(self):
        super(APIView, self).__init__()
        self.filter_dict = dict()

    # Return empty json with GET
    def get(self, request, format=None, **kwargs):
        return JsonResponse([], safe=False)

    def additional_list_logic(self, label_list, data_list):

        if self.xaxis is not 'dim_date__year_month_name':
            return label_list, data_list

        else:
            # Fill all the gap values with placeholder 0
            label_list_final = list()
            data_list_final = list()

            previous_val = 0
            for l, d in zip(label_list, data_list):

                current_val = int(l)
                for i in range(100):

                    # If no previous value or previous value + 1 = current value
                    if previous_val == 0 or previous_val + 1 == current_val:
                        label_list_final.append(l)
                        data_list_final.append(d)
                        break
                    else:
                        previous_val += 1
                        label_list_final.append(str(previous_val).zfill(2))
                        data_list_final.append(0)


                previous_val = current_val

            return label_list_final, data_list_final


    def set_filter_dict(self):
        # Include sales only
        self.filter_dict['movementtype'] = 'S'

        # Set order_by same as xaxis (level)
        self.order_by = self.xaxis

        # Define date range
        if self.kwargs.get('daterange_start') and self.kwargs.get('daterange_end'):
            daterange_start_temp = datetime.strptime(self.kwargs.get('daterange_start'), '%Y-%m-%d')
            daterange_end_temp = datetime.strptime(self.kwargs.get('daterange_end'), '%Y-%m-%d')
        else:
            daterange_start_temp = (datetime.today().replace(day=1) - timedelta(days=95)).replace(day=1)
            daterange_end_temp = datetime.today().replace(day=1) + timedelta(days=42)

        daterange_start = int(str(daterange_start_temp.year) + '{:02d}'.format(daterange_start_temp.month) + '{:02d}'.format(daterange_start_temp.day))
        self.filter_dict['dim_date_id__gte'] = daterange_start
        daterange_end = int(str(daterange_end_temp.year) + '{:02d}'.format(daterange_end_temp.month) + '{:02d}'.format(daterange_end_temp.day))
        self.filter_dict['dim_date_id__lt'] = daterange_end

        # # Big table query
        # data_list_query = models.FactMovements.objects.filter(**self.filter_dict).values(
        #     'dim_date__year_month_name'
        # ).annotate(
        #     sales_sum=Sum(aggregation)
        # ).order_by('dim_date__year_month_name')
        #
        # data_list_actual = list()
        # data_list_forecast = list()
        # label_list = list()
        # for data_dict in list(data_list_query):
        #     label_list.append(data_dict.get('dim_date__year_month_name'))
        #     data_list_actual.append(data_dict.get('sales_sum'))
        #     data_list_forecast.append(data_dict.get('sales_sum'))
        #
        # label_list += ['2018-02', '2018-03', '2018-04']
        # data_list_forecast += [250000, 23200, 323330]
        #
        # data = {
        #     'labels': label_list,
        #     'datasets': [
        #         {
        #             'label': 'Actual Sales',
        #             'lineTension': 0,
        #             'data': data_list_actual
        #         }, {
        #             'label': 'Forecast',
        #             'lineTension': 0,
        #             'fill': False,
        #             'backgroundColor': 'rgba(193, 66, 66, 0.3)',
        #             'borderColor': 'rgba(193, 66, 66, 0.70)',
        #             'pointBorderColor': 'rgba(193, 66, 66, 0.70)',
        #             'pointBackgroundColor': 'rgba(193, 66, 66, 0.70)',
        #             'pointHoverBackgroundColor': '#fff',
        #             'pointHoverBorderColor': 'rgba(191, 63, 63, 1)',
        #             'pointBorderWidth': 1,
        #             'data': data_list_forecast
        #         },
        #     ]
        # }
        # return data


class StoreAttributeTable(views.FormValidation):
    r"""
    View that shows/updates the store table
    """
    # Define variables
    form_class = forms.StoreForm
    model = models.DimStore


class SearchResultProduct(views.TableRead):
    r"""
    View that shows the content of the table
    """

    model = models.DimProduct
    limit = 3000
    format_list = ['image_url_link', None, None, None, None, None, None, None,]
    header_list = ['image', 'product code', 'style', 'colour', 'size', 'description', 'category', 'division',]
    form_field_list = [
        'image_url_link',
        'productcode',
        'style',
        'colour',
        'size',
        'productdescription',
        'category',
        'division',
    ]

    def set_filter_dict(self):
        query = Q(style=self.keyword)
        query.add(Q(productdescription=self.keyword), Q.OR)
        query.add(Q(colour=self.keyword), Q.OR)
        query.add(Q(category=self.keyword), Q.OR)
        query.add(Q(division=self.keyword), Q.OR)

        self.filter_dict = query


class SearchResultStore(views.TableRead):
    r"""
    View that shows the content of the table
    """

    model = models.DimStore
    limit = 3000
    format_list = ['link',  None, None, None, None, None, 'intcomma']
    header_list = ['link', 'store code', 'store name', 'store label', 'country', 'channel', 'size',]
    form_field_list = [
        'link',
        'store_code',
        'store_name',
        'store_display_label',
        [
            'dim_location',
            [
                'country',
            ],
        ],
        [
            'dim_channel',
            [
                'name',
            ],
        ],
        'store_size',
    ]

    def set_filter_dict(self):
        query = Q(store_name=self.keyword)
        query.add(Q(store_display_label=self.keyword), Q.OR)
        query.add(Q(dim_location__country=self.keyword), Q.OR)
        query.add(Q(dim_channel__name=self.keyword), Q.OR)

        self.filter_dict = query


r"""
Dashboards
"""
class StoreMap(views.WorldMap):
    r"""
    View that shows the store counts on a worldmap (map structure)
    """
    def get_context_dict(self, request, format=None, **kwargs):

        if self.kwargs.get('pk'):
            return {'height': '450'}

        model_obj = models.DimStore.objects.filter(is_active=True)
        label_list = model_obj.values_list(
              'dim_location__country',
              flat=True
        ).order_by('dim_location__country').distinct()
        data_list = list()
        total = 0
        for label in label_list:
            label_count = model_obj.filter(dim_location__country=label).count()
            total += label_count
            data_list.append({
                'label': label,
                'value': '{:,}'.format(label_count),
            })

        return {
            'height': '450',
            'title': 'Number of active stores',
            'total': '{:,}'.format(total),
            'table_items': data_list
        }


class StoreMapAPI(views.WorldMap):
    r"""
    View that shows the store counts on a worldmap (data)
    """

    def get(self, request, format=None, **kwargs):

        if self.kwargs.get('pk'):
            model_obj = models.DimStore.objects.filter(pk=self.kwargs.get('pk')).get()
            country = model_obj.dim_location.country_code_a2.lower()
            label_list = [country]
            data_dict = dict()
            data_dict[country] = str(1)
        else:
            model_obj = models.DimStore.objects.filter(is_active=True)
            label_list = sorted(list(set(model_obj.values_list('dim_location__country_code_a2', flat=True))), key=str.lower)
            label_list = [x.lower() for x in label_list]
            data_dict = dict()
            for label in label_list:
                data_dict[label] = str(model_obj.filter(dim_location__country_code_a2=label).count())

        return JsonResponse(data_dict, safe=False)


class HistoricalSalesTable(views.TableRead):
    r"""
    View that shows the content of the movements table (aggregated by channel and month)
    """

    model = models.FactMovements
    filter_dict = {
        'movementtype': 'S',
        # 'dim_date__id' + '__' + 'gte': 20160101,
        # 'dim_date__id' + '__' + 'lte': 20161231,
    }
    header_list = ['month', 'units', 'sales value (EUR)']
    aggregation_dict = {
        'values': ['dim_date__year_month_name',],
        'logic': {
            'units_sum': Sum('units'),
            'value_sum': Sum('salesvalue')
        }
    }
    format_list = [None, 'intcomma', 'intcomma']
    order_by = 'dim_date__year_month_name'


class HistoricalSalesChartAPI(views.ChartAPI):
    r'''
    View that provides the chart configuration and data
    '''
    # Variable definition
    model = models.FactMovements
    order_by = 'dim_date__year_month_name'
    xaxis = 'dim_date__year_month_name'
    chart_label = 'Sales'
    aggregation = 'units'

    def __init__(self):
        super(views.ChartAPI, self).__init__()
        self.filter_dict = dict()
        self.filter_dict['dim_date__id__gte'] = 20170101
        self.filter_dict['movementtype'] = 'S'


class ConsensusSalesChartAPI(views.ChartAPI):
    r'''
    View that provides the chart configuration and data
    '''
    # Variable definition
    model = models.PlanByMonth
    order_by = 'year_month_name_py'
    xaxis = 'year_month_name_py'
    chart_label = 'Sales'
    aggregation = 'units'

    def get(self, request, format=None, **kwargs):
        label_list = sorted(list(set(self.model.objects.values_list(self.xaxis, flat=True))))
        data_list_brand = list()
        data_list_store = list()
        data_list_consensus = list()

        for label in label_list:
            row = self.model.objects.filter(year_month_name_py=label).get()

            if self.kwargs.get('aggregation') == 'value':
                self.aggregation = 'value'
                data_list_brand.append(row.value_sales_py_product_category_level)
                data_list_store.append(row.value_sales_py_store_level)
                data_list_consensus.append(row.value_sales_py_year_month_level)
            else:
                data_list_brand.append(row.unit_sales_py_product_category_level)
                data_list_store.append(row.unit_sales_py_store_level)
                data_list_consensus.append(row.unit_sales_py_year_month_level)

        data = {
            'labels': label_list,
            'datasets': [
                {
                    'label': 'Brand',
                    'data': data_list_brand,
                    'backgroundColor': ['#cccccc' for x in list(range(len(label_list)))],
                    'borderColor': ['#918c8c' for x in list(range(len(label_list)))],
                    'borderWidth': 2
                },
                {
                    'label': 'Store',
                    'data': data_list_store,
                    'backgroundColor': ['#dddddd' for x in list(range(len(label_list)))],
                    'borderColor': ['#a4a1a1' for x in list(range(len(label_list)))],
                    'borderWidth': 2
                },
                {
                    'label': 'Consensus',
                    'data': data_list_consensus,
                    'backgroundColor': ['#EF8E3F' for x in list(range(len(label_list)))],
                    'borderColor': ['#c27434' for x in list(range(len(label_list)))],
                    'borderWidth': 2
                }
            ]
        }

        return JsonResponse(data, safe=False)


r"""
Store Clustering
"""
class StoreByClusterAIAPI(APIView):
    r'''
    View that provides the chart configuration and data
    '''

    def get(self, request, format=None, **kwargs):
        label_list = sorted(list(set(models.FeatureStoreInput.objects.values_list('cluster_ai', flat=True))), key=str.lower)

        data_list = list()
        for label in label_list:
            data_list.append(models.FeatureStoreInput.objects.filter(
                cluster_ai=label
            ).count())

        data = {
            'labels': label_list,
            'datasets': [
                {
                    'label': "Number of Stores",
                    'data': data_list
                }
            ]
        }
        return JsonResponse(data, safe=False)


class StoreByClusterUserAPI(APIView):
    r'''
    View that provides the chart configuration and data
    '''

    def get(self, request, format=None, **kwargs):
        label_list = sorted(list(set(models.FeatureStoreInput.objects.values_list('cluster_user', flat=True))), key=str.lower)
        data_list = list()
        for label in label_list:
            data_list.append(models.FeatureStoreInput.objects.filter(
                cluster_user=label
            ).count())

        data = {
            'labels': label_list,
            'datasets': [
                {
                    'label': "Number of stores",
                    'data': data_list
                }
            ]
        }
        return JsonResponse(data, safe=False)


class FeatureProductInputByClusterTable(views.TableRead):
    r"""
    View that shows the content of FeatureProductInputByCluster (populated by clustering workflow)
    """

    model = models.FeatureProductInputByCluster
    order_by = 'cluster'
    form_field_list = [
        'cluster',
        [
            'dim_product',
            [
                'productcode',
                'style',
                'productshortdescription',
                'division',
                'category',
                'colour',
                'size',
            ]
        ],
        'units',
        'salesvalueeur',
    ]

    format_list = [
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        'intcomma_rounding0',
        'intcomma_rounding0',
    ]


r"""
Sales Planning
"""
class SalesPlanChartAPI(APIView):
    r'''
    View that provides the chart configuration and data
    '''

    def get(self, request, format=None, **kwargs):

        aggregation = 'unit'
        if self.kwargs.get('aggregation') == 'value':
            aggregation = 'value'

        # Labels
        label_list = list()

        # Month
        data_list_query = models.PlanByMonth.objects.values(
            'year_month_name_py'
        ).annotate(
            sales_sum=Sum(aggregation + '_sales_py_year_month_level')
        ).order_by('year_month_name_py')

        data_list_month = list()
        for data_dict in list(data_list_query):
            label_list.append(data_dict.get('year_month_name_py'))
            data_list_month.append(data_dict.get('sales_sum'))

        # Store
        data_list_query = models.PlanByMonth.objects.values(
            'year_month_name_py'
        ).annotate(
            sales_sum=Sum(aggregation + '_sales_py_store_level')
        ).order_by('year_month_name_py')

        data_list_store = list()
        for data_dict in list(data_list_query):
            data_list_store.append(data_dict.get('sales_sum'))

        # Brand
        data_list_query = models.PlanByMonth.objects.values(
            'year_month_name_py'
        ).annotate(
            sales_sum=Sum(aggregation + '_sales_py_product_category_level')
        ).order_by('year_month_name_py')

        data_list_brand = list()
        for data_dict in list(data_list_query):
            data_list_brand.append(data_dict.get('sales_sum'))

        data = {
            'labels': label_list,
            'datasets': [
                {
                    'label': 'Plan Month',
                    'data': data_list_month,
                    'borderColor': '#4924CB',
                    'pointBorderColor': '#4924CB',
                    'backgroundColor': 'transparent',
                    'pointBackgroundColor': '#BC9EFF',
                },
                {
                    'label': 'Brand',
                    'data': data_list_brand,
                    'borderColor': '#631A09',
                    'pointBorderColor': '#631A09',
                    'backgroundColor': 'transparent',
                    'pointBackgroundColor': '#DB2500',
                },
                {
                    'label': 'Store',
                    'data': data_list_store,
                    'borderColor': '#0079FF',
                    'pointBorderColor': '#0079FF',
                    'backgroundColor': 'transparent',
                    'pointBackgroundColor': '#1B9DFF',
                }
            ]
        }
        return JsonResponse(data, safe=False)


class PlanByMonthTable(
    project_mixins_view.DMSFilter,
    views.TableRead,
):
    r"""
    View that shows the sales plan by month
    """

    model = models.PlanByMonth
    order_by = 'year_month_name_py'
    header_list = [
        'month LY',
        'units LY',
        'sales value LY (EUR)',
        'month PY',
        'units PY from brand plan',
        'sales value PY from brand plan (EUR)',
        'units PY from retail plan',
        'sales value PY from retail plan (EUR)',
        'units PY consensus',
        'sales value PY consensus (EUR)',
    ]
    format_list = [
        'input_key',
        'intcomma_rounding0',
        'intcomma_rounding0',
        None,
        'intcomma_rounding0',
        'intcomma_rounding0',
        'intcomma_rounding0',
        'intcomma_rounding0',
        'input_intcomma_rounding0',
        'input_intcomma_rounding0',
    ]
    tfoot = '1, 2, 4, 5, 6, 7, 8, 9'
    post_amends_filter_dict = False

    def set_form_field_list(self):
        self.form_field_list = [
            'year_month_name_ly',
            'unit_sales_ly',
            'value_sales_ly',
            'year_month_name_py',
            'unit_sales_py_product_category_level',
            'value_sales_py_product_category_level',
            'unit_sales_py_store_level',
            'value_sales_py_store_level',
            'unit_sales_py_year_month_level',
            'value_sales_py_year_month_level',
        ]

    def post_action(self):
        # Prepare POST data
        smart_save_input_dict = {
            'model': self.model._meta.db_table,
            'key_field': 'year_month_name_ly', # product_category
            'levels': ['year_month_name_ly'],
            'field_reference': {
                'unit_sales_ly': 'unit_sales_py_year_month_level',
            },
            'data': self.post_filter_dict
        }
        update_mix_index(smart_save_input_dict)


class PlanByProductCategoryTable(
    project_mixins_view.DMSFilter,
    views.TableRead
):
    r"""
    View that shows the sales plan by product category
    """

    model = models.PlanByProductCategory
    post_amends_filter_dict = False

    def prepare_variables(self):
        # Get level
        self.xaxis = self.kwargs.get('level', 0)
        self.order_by = self.xaxis

        # product_division
        if self.xaxis == 'product_division':
            self.header_list = [
                'product group',
                'units LY',
                'sales value LY (EUR)',
                'mix PY',
                'index PY',
                'units PY',
                'sales value PY (EUR)',
            ]
            self.format_list = [
                'input_key',
                'intcomma_rounding0',
                'intcomma_rounding0',
                'input_percentagecomma',
                'input_intcomma_rounding0',
                'intcomma_rounding0',
                'intcomma_rounding0',
            ]
            self.form_field_list = [
                'product_division',
                'unit_sales_ly',
                'value_sales_ly',
                'unit_sales_py_mix',
                'unit_sales_py_index',
                'unit_sales_py',
                'value_sales_py',
            ]
            self.tfoot = '1, 2, 3, 5, 6'
            self.aggregation_dict = {
                # 'values': ['dim_channel', 'sales_year', 'sales_season', 'product_division'],
                'values': ['product_division'],
                'logic': {
                    'unit_sales_ly_sum': Sum('unit_sales_ly'),
                    'value_sales_ly_sum': Sum('value_sales_ly'),
                    'unit_sales_py_mix_sum': Sum('unit_sales_py_mix'),
                    'unit_sales_py_index_min': Min('unit_sales_py_index'),
                    'unit_sales_py_sum': Sum('unit_sales_py'),
                    'value_sales_py_sum': Sum('value_sales_py'),
                }
            }

        # product_category (lowest level)
        else:
            self.header_list = [
                'product group',
                'product category',
                'units LY',
                'sales value LY (EUR)',
                'mix PY',
                'index PY',
                'units PY',
                'sales value PY (EUR)',
            ]
            self.format_list = [
                'input_key',
                'input_key',
                'intcomma_rounding0',
                'intcomma_rounding0',
                'input_percentagecomma',
                'input_intcomma_rounding0',
                'intcomma_rounding0',
                'intcomma_rounding0',
            ]
            self.form_field_list = [
                'product_division',
                'product_category',
                'unit_sales_ly',
                'value_sales_ly',
                'unit_sales_py_mix',
                'unit_sales_py_index',
                'unit_sales_py',
                'value_sales_py',
            ]
            self.tfoot = '2, 3, 6, 7'

    def post_action(self):
        # Prepare POST data
        smart_save_input_dict = {
            'model': self.model._meta.db_table,
            'key_field': self.xaxis, # product_category
            'levels': ['product_division', 'product_category',],
            'field_reference': {
                'unit_sales_py_index': 'unit_sales_py',
                'unit_sales_py_mix': 'unit_sales_py',
                'unit_sales_ly': 'unit_sales_py',
            },
            'data': self.post_filter_dict
        }
        update_mix_index(smart_save_input_dict)

        # Additional calculations (update consensus plan)
        total_unit_sales_py = self.model.objects.aggregate(Sum('unit_sales_py')).get('unit_sales_py__sum')
        total_value_sales_py = self.model.objects.aggregate(Sum('value_sales_py')).get('value_sales_py__sum')

        plan_month_queryset = models.PlanByMonth.objects
        total_unit_sales_ly = self.model.objects.aggregate(Sum('unit_sales_ly')).get('unit_sales_ly__sum')
        total_value_sales_ly = self.model.objects.aggregate(Sum('value_sales_ly')).get('value_sales_ly__sum')

        for item in plan_month_queryset.all():
            # unit_sales
            unit_sales_ly_percentage_by_month = item.unit_sales_ly/total_unit_sales_ly
            item.unit_sales_py_product_category_level = int(unit_sales_ly_percentage_by_month * total_unit_sales_py)
            # value_sales
            value_sales_ly_percentage_by_month = item.value_sales_ly/total_value_sales_ly
            item.value_sales_py_product_category_level = round(value_sales_ly_percentage_by_month * total_value_sales_py, 2)
            item.save()


class PlanByStoreTable(
    project_mixins_view.DMSFilter,
    views.TableRead
):
    r"""
    View that shows the sales plan by store
    """

    model = models.PlanByStore
    post_amends_filter_dict = False

    def prepare_variables(self):
        # Get level
        self.xaxis = self.kwargs.get('level', 0)
        self.order_by = self.xaxis

        # cluster_user
        if self.xaxis == 'cluster_user':
            self.header_list = [
                'cluster',
                'units LY',
                'sales value LY (EUR)',
                'mix PY',
                'index PY',
                'units PY',
                'sales value PY (EUR)',
            ]
            self.format_list = [
                'input_key',
                'intcomma_rounding0',
                'intcomma_rounding0',
                'input_percentagecomma',
                'input_intcomma_rounding0',
                'intcomma_rounding0',
                'intcomma_rounding0',
            ]
            self.form_field_list = [
                'cluster_user',
                'unit_sales_ly',
                'value_sales_ly',
                'unit_sales_py_mix',
                'unit_sales_py_index',
                'unit_sales_py',
                'value_sales_py',
            ]
            self.tfoot = '1, 2, 3, 5, 6'
            self.aggregation_dict = {
                'values': ['cluster_user'],
                'logic': {
                    'unit_sales_ly_sum': Sum('unit_sales_ly'),
                    'value_sales_ly_sum': Sum('value_sales_ly'),
                    'unit_sales_py_mix_sum': Sum('unit_sales_py_mix'),
                    'unit_sales_py_index_min': Min('unit_sales_py_index'),
                    'unit_sales_py_sum': Sum('unit_sales_py'),
                    'value_sales_py_sum': Sum('value_sales_py'),
                }
            }

        # dim_store__code (lowest level)
        else:
            self.header_list = [
                'cluster',
                'store code',
                'store name',
                'country',
                'units LY',
                'sales value LY (EUR)',
                'mix PY',
                'index PY',
                'units PY',
                'sales value PY (EUR)',
            ]
            self.format_list = [
                'input_key',
                'input_key',
                None,
                None,
                'intcomma_rounding0',
                'intcomma_rounding0',
                'input_percentagecomma',
                'input_intcomma_rounding0',
                'intcomma_rounding0',
                'intcomma_rounding0',
            ]
            self.form_field_list = [
                'cluster_user',
                'store_code',
                'store_name',
                'country',
                'unit_sales_ly',
                'value_sales_ly',
                'unit_sales_py_mix',
                'unit_sales_py_index',
                'unit_sales_py',
                'value_sales_py',
            ]
            self.tfoot = '4, 5, 8, 9'

    def post_action(self):
        # Prepare POST data
        smart_save_input_dict = {
            'model': self.model._meta.db_table,
            'key_field': self.xaxis, # product_category
            'levels': ['cluster_user', 'store_code',],
            'field_reference': {
                'unit_sales_py_index': 'unit_sales_py',
                'unit_sales_py_mix': 'unit_sales_py',
                'unit_sales_ly': 'unit_sales_py',
            },
            'data': self.post_filter_dict
        }
        update_mix_index(smart_save_input_dict)
        smart_save_input_dict = {
            'model': self.model._meta.db_table,
            'key_field': self.xaxis, # product_category
            'levels': ['cluster_user', 'store_code',],
            'field_reference': {
                'unit_sales_py_index': 'value_sales_py',
                'unit_sales_py_mix': 'value_sales_py',
                'value_sales_ly': 'value_sales_py',
            },
            'data': self.post_filter_dict
        }
        update_mix_index(smart_save_input_dict)

        # Additional calculations (update consensus plan)
        total_unit_sales_py = self.model.objects.aggregate(Sum('unit_sales_py')).get('unit_sales_py__sum')
        total_value_sales_py = self.model.objects.aggregate(Sum('value_sales_py')).get('value_sales_py__sum')

        plan_month_queryset = models.PlanByMonth.objects
        total_unit_sales_ly = self.model.objects.aggregate(Sum('unit_sales_ly')).get('unit_sales_ly__sum')
        total_value_sales_ly = self.model.objects.aggregate(Sum('value_sales_ly')).get('value_sales_ly__sum')

        for item in plan_month_queryset.all():
            # unit_sales
            unit_sales_ly_percentage_by_month = item.unit_sales_ly/total_unit_sales_ly
            item.unit_sales_py_store_level = int(unit_sales_ly_percentage_by_month * total_unit_sales_py)
            # value_sales
            value_sales_ly_percentage_by_month = item.value_sales_ly/total_value_sales_ly
            item.value_sales_py_store_level = round(value_sales_ly_percentage_by_month * total_value_sales_py, 2)
            item.save()


class RangeArchitectureTable(
    project_mixins_view.DMSFilter,
    views.TableRead
):
    r"""
    View that shows the range architecture
    """

    model = models.RangeArchitecture
    post_amends_filter_dict = False
    # page_length = 'unlimited'
    order_by = 'product_category'

    form_field_list = None
    format_list = [
        None, # product_division
        'input_key', # product_category

        'intcomma_rounding0', # range_width_style_ly_essential_basic
        'intcomma_rounding0', # range_width_style_ly_essential_fashion
        'intcomma_rounding0', # range_width_style_ly_trend_basic
        'intcomma_rounding0', # range_width_style_ly_trend_fashion
        'strong_intcomma_rounding0', # range_width_style_ly_total
        'input_intcomma_rounding0', # range_width_style_py_carry_over
        'input_intcomma_rounding0', # range_width_style_py_essential_basic
        'input_intcomma_rounding0', # range_width_style_py_essential_fashion
        'input_intcomma_rounding0', # range_width_style_py_trend_basic
        'input_intcomma_rounding0', # range_width_style_py_trend_fashion
        'strong_intcomma_rounding0', # range_width_style_py_total

        'intcomma_rounding0', # range_width_style_colour_ly_essential_basic
        'intcomma_rounding0', # range_width_style_colour_ly_essential_fashion
        'intcomma_rounding0', # range_width_style_colour_ly_trend_basic
        'intcomma_rounding0', # range_width_style_colour_ly_trend_fashion
        'strong_intcomma_rounding0', # range_width_style_colour_ly_total

        'intcomma_rounding0', # range_width_style_colour_py_carry_over
        'intcomma_rounding0', # range_width_style_colour_py_essential_basic
        'intcomma_rounding0', # range_width_style_colour_py_essential_fashion
        'intcomma_rounding0', # range_width_style_colour_py_trend_basic
        'intcomma_rounding0', # range_width_style_colour_py_trend_fashion
        'strong_intcomma_rounding0', # range_width_style_colour_py_total

        'intcomma_rounding0', # range_effectiveness_style_ly_essential_basic
        'intcomma_rounding0', # range_effectiveness_style_ly_essential_fashion
        'intcomma_rounding0', # range_effectiveness_style_ly_trend_basic
        'intcomma_rounding0', # range_effectiveness_style_ly_trend_fashion
        'strong_intcomma_rounding0', # range_effectiveness_style_ly_total

        'input_intcomma_rounding0', # range_effectiveness_style_py_carry_over
        'input_intcomma_rounding0', # range_effectiveness_style_py_essential_basic
        'input_intcomma_rounding0', # range_effectiveness_style_py_essential_fashion
        'input_intcomma_rounding0', # range_effectiveness_style_py_trend_basic
        'input_intcomma_rounding0', # range_effectiveness_style_py_trend_fashion
        'strong_intcomma_rounding0', # range_effectiveness_style_py_total

        'intcomma_rounding0', # range_performance_ly
        'input_intcomma_rounding0', # range_performance_py
    ]
    tfoot = '2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36'

    def post_action(self):
        product_category_list = self.post_filter_dict.get('product_category')
        range_width_style_py_carry_over_list = self.post_filter_dict.get('range_width_style_py_carry_over')
        range_width_style_py_essential_basic_list = self.post_filter_dict.get('range_width_style_py_essential_basic')
        range_width_style_py_essential_fashion_list = self.post_filter_dict.get('range_width_style_py_essential_fashion')
        range_width_style_py_trend_basic_list = self.post_filter_dict.get('range_width_style_py_trend_basic')
        range_width_style_py_trend_fashion_list = self.post_filter_dict.get('range_width_style_py_trend_fashion')

        range_effectiveness_style_py_carry_over_list = self.post_filter_dict.get('range_effectiveness_style_py_carry_over')
        range_effectiveness_style_py_essential_basic_list = self.post_filter_dict.get('range_effectiveness_style_py_essential_basic')
        range_effectiveness_style_py_essential_fashion_list = self.post_filter_dict.get('range_effectiveness_style_py_essential_fashion')
        range_effectiveness_style_py_trend_basic_list = self.post_filter_dict.get('range_effectiveness_style_py_trend_basic')
        range_effectiveness_style_py_trend_fashion_list = self.post_filter_dict.get('range_effectiveness_style_py_trend_fashion')

        range_performance_py_list = self.post_filter_dict.get('range_performance_py')

        for product_category, \
            range_width_style_py_carry_over, \
            range_width_style_py_essential_basic, \
            range_width_style_py_essential_fashion, \
            range_width_style_py_trend_basic, \
            range_width_style_py_trend_fashion, \
            range_effectiveness_style_py_carry_over, \
            range_effectiveness_style_py_essential_basic, \
            range_effectiveness_style_py_essential_fashion, \
            range_effectiveness_style_py_trend_basic, \
            range_effectiveness_style_py_trend_fashion, \
            range_performance_py, \
        in zip(
            product_category_list,
            range_width_style_py_carry_over_list,
            range_width_style_py_essential_basic_list,
            range_width_style_py_essential_fashion_list,
            range_width_style_py_trend_basic_list,
            range_width_style_py_trend_fashion_list,
            range_effectiveness_style_py_carry_over_list,
            range_effectiveness_style_py_essential_basic_list,
            range_effectiveness_style_py_essential_fashion_list,
            range_effectiveness_style_py_trend_basic_list,
            range_effectiveness_style_py_trend_fashion_list,
            range_performance_py_list,
        ):

            low_level_queryset = self.model.objects.get(
                dim_iapfilter=self.dim_iapfilter,
                product_category=product_category,
            )

            # range width - PY style level
            low_level_queryset.range_width_style_py_carry_over = int(range_width_style_py_carry_over.replace(',', ''))
            low_level_queryset.range_width_style_py_essential_basic = int(range_width_style_py_essential_basic.replace(',', ''))
            low_level_queryset.range_width_style_py_essential_fashion = int(range_width_style_py_essential_fashion.replace(',', ''))
            low_level_queryset.range_width_style_py_trend_basic = int(range_width_style_py_trend_basic.replace(',', ''))
            low_level_queryset.range_width_style_py_trend_fashion = int(range_width_style_py_trend_fashion.replace(',', ''))

            # range effectiveness - PY
            low_level_queryset.range_effectiveness_style_py_carry_over = int(range_effectiveness_style_py_carry_over.replace(',', ''))
            low_level_queryset.range_effectiveness_style_py_essential_basic = int(range_effectiveness_style_py_essential_basic.replace(',', ''))
            low_level_queryset.range_effectiveness_style_py_essential_fashion = int(range_effectiveness_style_py_essential_fashion.replace(',', ''))
            low_level_queryset.range_effectiveness_style_py_trend_basic = int(range_effectiveness_style_py_trend_basic.replace(',', ''))
            low_level_queryset.range_effectiveness_style_py_trend_fashion = int(range_effectiveness_style_py_trend_fashion.replace(',', ''))

            # range performance ASP PY
            low_level_queryset.range_performance_py = int(range_performance_py.replace(',', ''))

            # Save to database
            low_level_queryset.save()

        # Additional calculations
        for item in self.model.objects.all():

            # totals width style level
            item.range_width_style_ly_total = item.range_width_style_ly_essential_basic + item.range_width_style_ly_essential_fashion + item.range_width_style_ly_trend_basic + item.range_width_style_ly_trend_fashion
            item.range_width_style_py_total = item.range_width_style_py_essential_basic + item.range_width_style_py_essential_fashion + item.range_width_style_py_trend_basic + item.range_width_style_py_trend_fashion + item.range_width_style_py_carry_over

            # range width - LY style colour level
            item.range_width_style_colour_py_carry_over = 0 * item.range_width_style_py_carry_over
            item.range_width_style_colour_py_essential_basic = item.range_width_style_ly_essential_basic_avg_colour_count * item.range_width_style_py_essential_basic
            item.range_width_style_colour_py_essential_fashion = item.range_width_style_ly_essential_fashion_avg_colour_count * item.range_width_style_py_essential_fashion
            item.range_width_style_colour_py_trend_basic = item.range_width_style_ly_trend_basic_avg_colour_count * item.range_width_style_py_trend_basic
            item.range_width_style_colour_py_trend_fashion = item.range_width_style_ly_trend_fashion_avg_colour_count * item.range_width_style_py_trend_fashion
            item.range_width_style_colour_py_total = item.range_width_style_colour_py_carry_over + item.range_width_style_colour_py_essential_basic + item.range_width_style_colour_py_essential_fashion + item.range_width_style_colour_py_trend_basic + item.range_width_style_colour_py_trend_fashion

            # totals effectiveness style level
            item.range_effectiveness_style_ly_total = item.range_effectiveness_style_ly_essential_basic + item.range_effectiveness_style_ly_essential_fashion + item.range_effectiveness_style_ly_trend_basic + item.range_effectiveness_style_ly_trend_fashion
            item.range_effectiveness_style_py_total = item.range_effectiveness_style_py_carry_over + item.range_effectiveness_style_py_essential_basic + item.range_effectiveness_style_py_essential_fashion + item.range_effectiveness_style_py_trend_basic + item.range_effectiveness_style_py_trend_fashion

            item.save()


class StrategicSalesPlanTable(views.TableRead):
    r"""
    View that shows the strategic sales plan
    """

    model = models.StrategicSalesPlan
    post_amends_filter_dict = False
    page_length = 'unlimited'

    def prepare_variables(self):
        # Get level
        self.xaxis = self.kwargs.get('level', 0)
        self.order_by = self.xaxis

        # sales_season
        if self.xaxis == 'sales_season':
            self.filter_dict = {
                'sales_year__gte': 2018
            }

            self.header_list = [
                'plan year',
                'sales season',
                'seasonal mix',
                'gross sales',
                'discounts',
                'returns',
                'net sales',
                'ASP',
                'gross sales per unit',
                'sell-through ratio',
                'sell-in',
                'mark-up',
                'gross margin %',
                'gross margin value',
                'buying budget',
                'GMROI % target',
                'beginning season inventory',
                'markdown',
                'ending season inventory',
                'average cost of inventory',
                'intake beginning of season',
            ]
            self.form_field_list = [
                'row_styling',
                'sales_year',
                'region',
                'gross_sales_index',
                'gross_sales',
                'discounts',
                'returns',
                'net_sales',
                'asp',
                'gross_sales_per_unit',
                'sell_through_ratio',
                'sell_in',
                'markup',
                'gross_margin_percentage',
                'gross_margin',
                'buying_budget',
                'gmroi_percentage_target',
                'beginning_season_inventory',
                'markdown',
                'ending_season_inventory',
                'average_cost_of_inventory',
                'intake_beginning_of_season',
            ]
            self.format_list = [
                'skip',
            	'input_key', # sales_year
            	'input_key', # sales_season
            	'input_percentagecomma', # seasonal_mix
            	'intcomma_rounding0', # gross_sales
            	'input_intcomma_rounding0', # discounts
            	'input_intcomma_rounding0', # returns
                'intcomma_rounding0', # net_sales
                'intcomma_rounding0', # asp
            	'intcomma_rounding0', # gross_sales_per_unit
                'input_intcomma_rounding0', # sell_through_ratio
            	'intcomma_rounding0', # sell_in
            	'input_intcomma_rounding0', # markup
            	'input_percentagecomma', # gross_margin_percentage
            	'intcomma_rounding0', # gross_magin_value
            	'intcomma_rounding0', # buying_budget
            	'input_percentagecomma', # gmroi_percentage_target
            	'intcomma_rounding0', # beginning_season_inventory
            	'input_intcomma_rounding0', # markdown
            	'intcomma_rounding0', # ending_season_inventory
                'intcomma_rounding0', # average_cost_of_inventory
                'intcomma_rounding0', # intake_beginning_of_season
            ]
            self.tfoot = '3, 4, 5, 6, 13, 14, 16, 17, 18, 20'
            self.aggregation_dict = {
                'values': ['row_styling', 'sales_year', 'sales_season'],
                'logic': {
                    'seasonal_mix_min': Min('seasonal_mix'), # input
                    'gross_sales_sum': Sum('gross_sales'),
                    'discounts_sum': Sum('discounts'), # input
                    'returns_sum': Sum('returns'), # input
                    'net_sales_sum': Sum('net_sales'),
                    'asp_sum': Sum('asp'),
                    'gross_sales_per_unit_sum': Sum('gross_sales_per_unit'),
                    'sell_through_ratio_min': Min('sell_through_ratio'), # input
                    'sell_in_sum': Sum('sell_in'),
                    'markup_sum': Max('markup'), # input
                    'gross_margin_percentage_sum': Max('gross_margin_percentage'),
                    'gross_margin_sum': Sum('gross_margin'),
                    'buying_budget_sum': Sum('buying_budget'),
                    'gmroi_percentage_target_sum': Max('gmroi_percentage_target'),
                    'beginning_season_inventory_sum': Sum('beginning_season_inventory'),
                    'markdown_sum': Sum('markdown'),
                    'ending_season_inventory_sum': Sum('ending_season_inventory'),
                    'average_cost_of_inventory': Sum('average_cost_of_inventory'),
                    'intake_beginning_of_season': Sum('intake_beginning_of_season'),
                }
            }

        # sales_season
        elif self.xaxis == 'dim_channel__name':
            self.filter_dict = {
                'sales_year__gte': 2018
            }

            self.header_list = [
                'plan year',
                'sales season',
                'channel mix',
                'gross sales',
                'discounts',
                'returns',
                'net sales',
                'ASP',
                'gross sales per unit',
                'sell-through ratio',
                'sell-in',
                'mark-up',
                'gross margin %',
                'gross margin value',
                'buying budget',
                'GMROI % target',
                'beginning season inventory',
                'markdown',
                'ending season inventory',
                'average cost of inventory',
                'intake beginning of season',
            ]
            self.form_field_list = [
                'row_styling',
                'sales_year',
                'channel',
                'gross_sales_index',
                'gross_sales',
                'discounts',
                'returns',
                'net_sales',
                'asp',
                'gross_sales_per_unit',
                'sell_through_ratio',
                'sell_in',
                'markup',
                'gross_margin_percentage',
                'gross_margin',
                'buying_budget',
                'gmroi_percentage_target',
                'beginning_season_inventory',
                'markdown',
                'ending_season_inventory',
                'average_cost_of_inventory',
                'intake_beginning_of_season',
            ]
            self.format_list = [
                'skip',
            	'input_key', # sales_year
            	'input_key', # sales_season
            	'input_percentagecomma', # channel_mix
            	'intcomma_rounding0', # gross_sales
            	'input_intcomma_rounding0', # discounts
            	'input_intcomma_rounding0', # returns
                'intcomma_rounding0', # net_sales
                'intcomma_rounding0', # asp
            	'intcomma_rounding0', # gross_sales_per_unit
                'input_intcomma_rounding0', # sell_through_ratio
            	'intcomma_rounding0', # sell_in
            	'input_intcomma_rounding0', # markup
            	'input_percentagecomma', # gross_margin_percentage
            	'intcomma_rounding0', # gross_magin_value
            	'intcomma_rounding0', # buying_budget
            	'input_percentagecomma', # gmroi_percentage_target
            	'intcomma_rounding0', # beginning_season_inventory
            	'input_intcomma_rounding0', # markdown
            	'intcomma_rounding0', # ending_season_inventory
                'intcomma_rounding0', # average_cost_of_inventory
                'intcomma_rounding0', # intake_beginning_of_season
            ]
            self.tfoot = '3, 4, 5, 6, 13, 14, 16, 17, 18, 20'
            self.aggregation_dict = {
                'values': ['row_styling', 'sales_year', 'dim_channel__name'],
                'logic': {
                    'channel_mix_min': Min('channel_mix'), # input
                    'gross_sales_sum': Sum('gross_sales'),
                    'discounts_sum': Sum('discounts'), # input
                    'returns_sum': Sum('returns'), # input
                    'net_sales_sum': Sum('net_sales'),
                    'asp_sum': Sum('asp'),
                    'gross_sales_per_unit_sum': Sum('gross_sales_per_unit'),
                    'sell_through_ratio_min': Min('sell_through_ratio'), # input
                    'sell_in_sum': Sum('sell_in'),
                    'markup_sum': Max('markup'), # input
                    'gross_margin_percentage_sum': Max('gross_margin_percentage'),
                    'gross_margin_sum': Sum('gross_margin'),
                    'buying_budget_sum': Sum('buying_budget'),
                    'gmroi_percentage_target_sum': Max('gmroi_percentage_target'),
                    'beginning_season_inventory_sum': Sum('beginning_season_inventory'),
                    'markdown_sum': Sum('markdown'),
                    'ending_season_inventory_sum': Sum('ending_season_inventory'),
                    'average_cost_of_inventory': Sum('average_cost_of_inventory'),
                    'intake_beginning_of_season': Sum('intake_beginning_of_season'),
                }
            }

        # sales_year and region
        elif self.xaxis == 'sales_year':
            self.header_list = [
                'plan year',
                'region',
                'gross sales index',
                'gross sales',
                'discounts',
                'returns',
                'net sales',
                'ASP',
                'gross sales per unit',
                'sell-through ratio',
                'sell-in',
                'mark-up',
                'gross margin %',
                'gross margin value',
                'buying budget',
                'GMROI % target',
                'beginning season inventory',
                'markdown',
                'ending season inventory',
                'average cost of inventory',
                'intake beginning of season',
            ]
            self.form_field_list = [
                'row_styling',
                'sales_year',
                'region',
                'gross_sales_index',
                'gross_sales',
                'discounts',
                'returns',
                'net_sales',
                'asp',
                'gross_sales_per_unit',
                'sell_through_ratio',
                'sell_in',
                'markup',
                'gross_margin_percentage',
                'gross_margin',
                'buying_budget',
                'gmroi_percentage_target',
                'beginning_season_inventory',
                'markdown',
                'ending_season_inventory',
                'average_cost_of_inventory',
                'intake_beginning_of_season',
            ]
            self.format_list = [
                'skip',
            	'input_key', # sales_year
            	'input_key', # region
            	'input_intcomma_rounding0', # gross_sales_index
            	'intcomma_rounding0', # gross_sales
            	'input_intcomma_rounding0', # discounts
            	'input_intcomma_rounding0', # returns
                'intcomma_rounding0', # net_sales
                'intcomma_rounding0', # asp
            	'intcomma_rounding0', # gross_sales_per_unit
                'input_intcomma_rounding0', # sell_through_ratio
            	'intcomma_rounding0', # sell_in
            	'input_intcomma_rounding0', # markup
            	'input_percentagecomma', # gross_margin_percentage
            	'intcomma_rounding0', # gross_magin_value
            	'intcomma_rounding0', # buying_budget
            	'input_percentagecomma', # gmroi_percentage_target
            	'intcomma_rounding0', # beginning_season_inventory
            	'input_intcomma_rounding0', # markdown
            	'intcomma_rounding0', # ending_season_inventory
                'intcomma_rounding0', # average_cost_of_inventory
                'intcomma_rounding0', # intake_beginning_of_season
            ]
            self.tfoot = '3, 4, 5, 6, 13, 14, 16, 17, 18, 20'
            self.aggregation_dict = {
                'values': ['row_styling', 'sales_year', 'region'],
                'logic': {
                    'gross_sales_index_min': Min('gross_sales_index'), # input
                    'gross_sales_sum': Sum('gross_sales'),
                    'discounts_sum': Sum('discounts'), # input
                    'returns_sum': Sum('returns'), # input
                    'net_sales_sum': Sum('net_sales'),
                    'asp_sum': Sum('asp'),
                    'gross_sales_per_unit_sum': Sum('gross_sales_per_unit'),
                    'sell_through_ratio_min': Min('sell_through_ratio'), # input
                    'sell_in_sum': Sum('sell_in'),
                    'markup_sum': Max('markup'), # input
                    'gross_margin_percentage_sum': Max('gross_margin_percentage'),
                    'gross_margin_sum': Sum('gross_margin'),
                    'buying_budget_sum': Sum('buying_budget'),
                    'gmroi_percentage_target_sum': Max('gmroi_percentage_target'),
                    'beginning_season_inventory_sum': Sum('beginning_season_inventory'),
                    'markdown_sum': Sum('markdown'),
                    'ending_season_inventory_sum': Sum('ending_season_inventory'),
                    'average_cost_of_inventory': Sum('average_cost_of_inventory'),
                    'intake_beginning_of_season': Sum('intake_beginning_of_season'),
                }
            }

    def post_action(self):
        # Prepare POST data
        empty_list = [None for v in self.post_filter_dict.get('sales_year')]
        sales_year_list = self.post_filter_dict.get('sales_year')
        sales_season_list = self.post_filter_dict.get('sales_season', empty_list)
        region_list = self.post_filter_dict.get('region', empty_list)
        channel_list = self.post_filter_dict.get('channel', empty_list)
        seasonal_mix_list = self.post_filter_dict.get('seasonal_mix', empty_list)
        channel_mix_list = self.post_filter_dict.get('channel_mix', empty_list)
        gross_sales_index_list = self.post_filter_dict.get('gross_sales_index', empty_list)
        discounts_list = self.post_filter_dict.get('discounts')
        returns_list = self.post_filter_dict.get('returns')
        sell_through_ratio_list = self.post_filter_dict.get('sell_through_ratio')
        markup_list = self.post_filter_dict.get('markup')
        gross_margin_percentage_list = self.post_filter_dict.get('gross_margin_percentage')
        gmroi_percentage_target_list = self.post_filter_dict.get('gmroi_percentage_target')
        markdown_list = self.post_filter_dict.get('markdown')

        for sales_year, sales_season, region, channel, seasonal_mix, channel_mix, gross_sales_index, discounts, returns, sell_through_ratio, markup, gross_margin_percentage, gmroi_percentage_target, markdown in zip(
            sales_year_list,
            sales_season_list,
            region_list,
            channel_list,
            seasonal_mix_list,
            channel_mix_list,
            gross_sales_index_list,
            discounts_list,
            returns_list,
            sell_through_ratio_list,
            markup_list,
            gross_margin_percentage_list,
            gmroi_percentage_target_list,
            markdown_list
        ):

            if region:
                high_level_queryset = self.model.objects.filter(sales_year=sales_year, region=region)
            elif sales_season:
                high_level_queryset = self.model.objects.filter(sales_year=sales_year, sales_season=sales_season)
            elif channel:
                high_level_queryset = self.model.objects.filter(sales_year=sales_year, channel=channel)
            else:
                break

            sum_gross_sales_init = high_level_queryset.aggregate(Sum('gross_sales_init')).get('gross_sales_init__sum')
            sum_discounts = high_level_queryset.aggregate(Sum('discounts')).get('discounts__sum')
            sum_returns = high_level_queryset.aggregate(Sum('returns')).get('returns__sum')
            sum_markdown = high_level_queryset.aggregate(Sum('markdown')).get('markdown__sum')

            for low_level in high_level_queryset.all():
                low_level_queryset = self.model.objects.get(
                    sales_year=sales_year,
                    region=region,
                    sales_season=low_level.sales_season,
                    dim_channel=low_level.dim_channel,
                )

                # discounts
                if sum_discounts > 0:
                    low_level_queryset.discounts = int(discounts.replace(',', '')) * low_level_queryset.discounts/sum_discounts
                else:
                    low_level_queryset.discounts = int(discounts.replace(',', '')) / high_level_queryset.count()

                # returns
                if sum_returns > 0:
                    low_level_queryset.returns = int(returns.replace(',', '')) * low_level_queryset.returns/sum_returns
                else:
                    low_level_queryset.returns = int(returns.replace(',', '')) / high_level_queryset.count()

                # markdown
                if sum_markdown > 0:
                    low_level_queryset.markdown = int(markdown.replace(',', '')) * low_level_queryset.markdown/sum_markdown
                else:
                    low_level_queryset.markdown = int(markdown.replace(',', '')) / high_level_queryset.count()

                if sum_gross_sales_init > 0:
                    # gross_sales_index
                    if gross_sales_index:
                        low_level_queryset.gross_sales_index = int(gross_sales_index.replace(',', ''))
                    # seasonal_mix
                    if seasonal_mix:
                        low_level_queryset.seasonal_mix = convert_percentage(seasonal_mix.replace(',', ''))
                    # seasonal_mix
                    if channel_mix:
                        low_level_queryset.channel_mix = convert_percentage(channel_mix.replace(',', ''))

                # gross_sales
                low_level_queryset.gross_sales = sum_gross_sales_init * low_level_queryset.gross_sales_index * low_level_queryset.seasonal_mix * low_level_queryset.channel_mix

                # sell_through_ratio
                low_level_queryset.sell_through_ratio = int(sell_through_ratio.replace(',', ''))
                # markup
                low_level_queryset.markup = int(markup.replace(',', ''))
                # gross_margin_percentage
                low_level_queryset.gross_margin_percentage = convert_percentage(gross_margin_percentage.replace(',', ''))
                # gmroi_percentage_target
                low_level_queryset.gmroi_percentage_target = convert_percentage(gmroi_percentage_target.replace(',', ''))

                # Save to database
                low_level_queryset.save()

        # Additional calculations
        for item in self.model.objects.all():
            item.gross_sales = item.gross_sales_init * item.gross_sales_index
            item.net_sales = item.gross_sales - item.discounts - item.returns
            item.sell_in = item.net_sales * item.sell_through_ratio
            item.gross_margin = item.net_sales * item.gross_margin_percentage
            item.gross_sales_per_unit = item.gross_sales / item.asp
            item.buying_budget = item.sell_in / item.markup if item.markup > 0 else item.sell_in
            item.beginning_season_inventory = 0
            item.ending_season_inventory = item.beginning_season_inventory - item.net_sales - item.markdown
            item.save()


class RangePlanTable(
    project_mixins_view.DMSFilter,
    views.TableRead
):
    r"""
    View that shows the range architecture
    """

    model = models.RangePlan
    post_amends_filter_dict = False
    # page_length = 'unlimited'
    order_by = 'product_category'

    form_field_list = None
    format_list = [
        None, # product_division
        'input_key', # product_category
        'input_key', # product_essential_trend
        'input_key', # product_basic_fashion

        'intcomma_rounding0', # range_width_style_py_rangearchitecture
        'intcomma_rounding0', # range_width_style_py_rangearchitecture_style_colour_count
        'intcomma_rounding0', # range_width_style_py_rangemaster
        'intcomma_rounding0', # range_width_style_colour_py_rangemaster
    ]
    tfoot = '4, 5, 6, 7'

    def pre_action(self):

        # update table based on rangearchitecture
        for item in self.model.objects.filter(dim_iapfilter=self.dim_iapfilter).all():

            # rangearchitecture fields
            rangearchitecture = models.RangeArchitecture.objects.get(
                dim_iapfilter=item.dim_iapfilter,
                product_category=item.product_category,
            )

            if item.product_essential_trend == 'E' and item.product_basic_fashion == 'B':
                item.range_width_style_py_rangearchitecture = rangearchitecture.range_width_style_py_essential_basic
                item.range_width_style_colour_py_rangearchitecture = rangearchitecture.range_width_style_colour_py_essential_basic
            if item.product_essential_trend == 'E' and item.product_basic_fashion == 'F':
                item.range_width_style_py_rangearchitecture = rangearchitecture.range_width_style_py_essential_fashion
                item.range_width_style_colour_py_rangearchitecture = rangearchitecture.range_width_style_colour_py_essential_fashion
            if item.product_essential_trend == 'T' and item.product_basic_fashion == 'B':
                item.range_width_style_py_rangearchitecture = rangearchitecture.range_width_style_py_trend_basic
                item.range_width_style_colour_py_rangearchitecture = rangearchitecture.range_width_style_colour_py_trend_basic
            if item.product_essential_trend == 'T' and item.product_basic_fashion == 'F':
                item.range_width_style_py_rangearchitecture = rangearchitecture.range_width_style_py_trend_fashion
                item.range_width_style_colour_py_rangearchitecture = rangearchitecture.range_width_style_colour_py_trend_fashion

            # rangemaster fields
            rangemaster = models.RangeMaster.objects.filter(
                dim_iapfilter=item.dim_iapfilter,
                product_category=item.product_category,
            )

            item.range_width_style_py_rangemaster = rangemaster.filter(
                product_essential_trend=item.product_essential_trend,
                product_basic_fashion=item.product_basic_fashion,
            ).values('style_number').distinct().count()

            item.range_width_style_colour_py_rangemaster = rangemaster.filter(
                product_essential_trend=item.product_essential_trend,
                product_basic_fashion=item.product_basic_fashion,
            ).count()

            item.save()


class RangeAssortmentTable(
    project_mixins_view.DMSFilter,
    views.TableRead
):
    r"""
    View that shows the range architecture
    """

    model = models.RangeAssortment
    post_amends_filter_dict = True
    # page_length = 'unlimited'
    order_by = 'product_category'

    form_field_list = None
    format_list = [
        'input_key', # cluster_user
        None, # product_division
        'input_key', # product_category
        'input_key', # product_essential_trend
        'input_key', # product_basic_fashion
        'intcomma_rounding0', # range_width_style_ly_storecluster
        'intcomma_rounding0', # range_width_style_colour_ly_storecluster
        'input_intcomma_rounding0', # range_width_style_py
        'input_intcomma_rounding0', # range_width_style_colour_py
    ]
    tfoot = '5, 6, 7, 8'

    # Return empty table GET
    def get(self, request):
        self.context_dict = {
            'message': {
                'text': 'Table will be loaded after clicking the "Refresh" button.',
                'type': 'info',
                'position_left': True,
            }
        }
        return self.display(request)

    # Overwrite variables
    def set_filter_dict(self):
        pass

    def post_action(self):
        cluster_user_list = self.post_filter_dict.get('cluster_user')
        product_category_list = self.post_filter_dict.get('product_category')
        product_essential_trend_list = self.post_filter_dict.get('product_essential_trend')
        product_basic_fashion_list = self.post_filter_dict.get('product_basic_fashion')

        range_width_style_py_list = self.post_filter_dict.get('range_width_style_py')
        range_width_style_colour_py_list = self.post_filter_dict.get('range_width_style_colour_py')

        if cluster_user_list and product_category_list and product_essential_trend_list and product_basic_fashion_list:

            for cluster_user, \
                product_category, \
                product_essential_trend, \
                product_basic_fashion, \
                range_width_style_py, \
                range_width_style_colour_py, \
            in zip(
                cluster_user_list,
                product_category_list,
                product_essential_trend_list,
                product_basic_fashion_list,
                range_width_style_py_list,
                range_width_style_colour_py_list,
            ):

                low_level_queryset = self.model.objects.get(
                    dim_iapfilter=self.dim_iapfilter,
                    product_category=product_category,
                    product_essential_trend=product_essential_trend,
                    product_basic_fashion=product_basic_fashion,
                    cluster_user=cluster_user,
                )

                # range width - PY style level
                low_level_queryset.range_width_style_py = int(range_width_style_py.replace(',', ''))
                low_level_queryset.range_width_style_colour_py = int(range_width_style_colour_py.replace(',', ''))

                # Save to database
                low_level_queryset.save()


class TokenFieldDimProductStyle(views.TokenFieldAPI):
    r"""
    View that loads the data for tokenfield.
    """
    model = models.DimProduct
    field_name = 'style'


class IAPCycleUpdate(
    project_mixins_view.DMSFilter,
    views.SimpleUpdate
):
    r"""
    View that does a simple update according to pk and target field(s)
    """
    # Define variables
    model = models.DimIAPCycle

    def business_logic(self):
        # Get kwargs
        dim_iapcycle_id = self.kwargs.get('dim_iapcycle_id')
        is_completed = self.kwargs.get('is_completed', False)

        # Get model values
        model = self.model.objects.filter(pk=dim_iapcycle_id)
        queryset = model.get()
        dim_iapstep_id = queryset.dim_iapstep.id
        dim_iapstep_position = queryset.dim_iapstep.position

        # Update model
        model.update(
            is_completed=is_completed,
            completion_dt=timezone.now()
        )

        # Create new model entry
        if is_completed == 1:
            # Check if next step exists
            next_position = dim_iapstep_position + 1
            next_dim_iapstep = models.DimIAPStep.objects.filter(position=next_position)
            if next_dim_iapstep.exists():
                # Get next pk
                next_dim_iapstep_id = next_dim_iapstep.get().id
                entry = self.model.objects.update_or_create(
                    dim_iapfilter_id=self.dim_iapfilter,
                    dim_iapstep_id=next_dim_iapstep_id
                )
        # Set all next steps to False
        else:
            self.model.objects.filter(dim_iapstep__position__gt=dim_iapstep_position).update(
                is_completed=False,
                completion_dt=None,
            )

        return is_completed


class IAPFilterUserUpdate(
    project_mixins_view.DMSFilter,
    views.SimpleUpdate
):
    r"""
    View that does a simple update according to pk and target field(s)
    """
    # Define variables
    model = models.DimIAPFilterUser

    def business_logic(self, request):
        post_data = request.POST

        # Read POST variables
        dim_channel_id = post_data.get('dim_channel_id')
        sales_year = post_data.get('sales_year')
        sales_season = post_data.get('sales_season')

        dim_iapfilter = models.DimIAPFilter.objects.filter(
            dim_channel_id=dim_channel_id,
            sales_year=sales_year,
            sales_season=sales_season,
        ).first()

        user_filter_query = self.model.objects.filter(
            user=request.user,
        ).update(dim_iapfilter=dim_iapfilter)

        return True


class StoredProcedureAPI(
    project_mixins_view.DMSFilter,
    mixins_apiview.StoredProcedureAPI
):
    r"""
    View that runs the RPC
    """

    def get_model_obj(self, param):
        if param == 'generate_consolidated_plan':
            self.filter_dict = dict()
            self.init_class_dict_mixin()
            file_path_abs = os.path.join(cp.UPLOAD_URL_ABS, r'''plans''', self.consolidated_plan_file)
            calls.generate_consolidated_plan(self.dim_iapfilter, file_path_abs)
        else:
            return getattr(calls, param)()


class StoredProcedureList(views.TableProcedure, mixins_view.SecurityModelNameMixin):
    r"""
    View that shows the Console stored procedures that a user can run
    """

    user_permission_model = UserPermissions
    group_permission_model = GroupPermissions
    target_model = Item
    permission_type = ['procedure', 'rpc']

    def get_context_dict(self, request):

        # Get procedure name list
        self.set_user(request.user)
        procedure_name_list = self.get_authorized_model_item_list()

        procedure_list = list()
        for procedure_name in procedure_name_list:
            item = Item.objects.get(permission_type__in=self.permission_type, name=procedure_name)

            procedure_list.append({
                'number': item.sequence,
                'name': item.name,
                'label': item.label,
                'url': reverse_lazy('procedure_run', kwargs={'item': item.name}),
                'duration': item.duration,
                'completion_percentage': item.completion_percentage,
                'completion_dt': item.end_dt
            })

        procedure_list = sorted(procedure_list, key=lambda k: k['number'])

        return {
            'form_items': procedure_list,
            'message': {
                'text': 'No procedure available',
                'type': 'warning',
                'position_left': True
            }
        }


class DownloadScreen(
    project_mixins_view.DMSFilter,
    views.SimpleBlockView
):
    r"""
    View that displays the uploaded image
    """

    # model = models.PlanByMonthProductCategoryStore
    template_name = 'blocks/download_screen.html'

    def get_context_dict(self, request):

        # Get file name
        file_path_abs = os.path.join(cp.UPLOAD_URL_ABS, r'''plans''', self.consolidated_plan_file)
        file_path_rel = os.path.join(cp.UPLOAD_URL, r'''plans''', self.consolidated_plan_file)

        # If the Excel file exists for download
        if os.path.isfile(file_path_abs):
            # Prepare context object
            image_context_dict = dict()
            image_context_dict['download_file'] = file_path_rel
            return image_context_dict

        # If user has not generated the file yet
        else:
            return {
                'message': {
                    'text': '<p><strong>Excel file was not generated.</strong></p><p>Run the procedure and refresh this panel.</p>',
                    'type': 'info',
                    'position_left': True,
                }
            }


class ConsolidatedPlanPivotTable(
    project_mixins_view.DMSFilter,
    views.PivotTableAPI
):
    r"""
    View that shows the content of the pivot table
    """

    model = models.PlanByMonthProductCategoryStore
    header_dict = {
        'year_month_name_py': 'month PY',
        'cluster_user': 'cluster',
        'dim_store__store_name': 'store name',
        'dim_store__dim_location__country': 'store country',
        'product_category': 'product category',
        'product_division': 'product division',
        'unit_sales_py_sum': 'unit sales',
        'value_sales_py_sum': 'value sales',
    }
    aggregation_dict = {
        'values': [
            'year_month_name_py',
            'cluster_user',
            'dim_store__store_name',
            'dim_store__dim_location__country',
            'product_category',
            'product_division',
        ],
        'logic': {
            'unit_sales_py_sum': Sum('unit_sales_py'),
            'value_sales_py_sum': Sum('value_sales_py'),
        }
    }

    def set_filter_dict(self):
        self.filter_dict = dict()
        # self.filter_dict['dim_iapfilter'] = self.dim_iapfilter
