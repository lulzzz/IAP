from datetime import datetime, timedelta

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.conf import settings as cp

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

from . import models
from . import forms
from . import serializers
from . import mixins_view as project_mixins_view

from workflows.core.hierarchy_utils import update_mix_index

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
        'units PY',
        'sales value PY (EUR)',
    ]
    format_list = [
        'input_key',
        'intcomma_rounding0',
        'intcomma_rounding0',
        None,
        'input_intcomma_rounding0',
        'input_intcomma_rounding0',
    ]
    tfoot = '1, 2, 4, 5'
    post_amends_filter_dict = False

    def set_form_field_list(self):
        self.form_field_list = [
            'year_month_name_ly',
            'unit_sales_ly',
            'value_sales_ly',
            'year_month_name_py',
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
            self.tfoot = '1, 2, 5, 6'
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
            self.tfoot = '1, 2, 5, 6'
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


class RangeArchitectureTable(
    project_mixins_view.DMSFilter,
    views.TableRead
):
    r"""
    View that shows the range architecture
    """

    model = models.RangeArchitecture
    post_amends_filter_dict = False
    order_by = 'product_category'
    # header_list = [
    #     'product group',
    #     'product category',
    #     'essential trend',
    #     'basic fashion',
    #     'units LY',
    #     'sales value LY (EUR)',
    #     'mix PY',
    #     'index PY',
    #     'units PY',
    #     'sales value PY (EUR)',
    # ]
    format_list = [
        None,
        None,
        None,
        None,
        'intcomma_rounding0',
        'intcomma_rounding0',
        'intcomma_rounding0',
        'input_intcomma_rounding0',
        'input_intcomma_rounding0',
    ]
    tfoot = '6, 8'

    def set_form_field_list(self):
        self.form_field_list = [
            'product_division',
            'product_category',
            'product_essential_trend',
            'product_basic_fashion',
            'range_width_style_ly',
            'range_width_style_colour_ly',
            'range_depth_ly',
            'range_width_style_py',
            'range_depth_py',
        ]

    def post_action(self):
        # Clear GET filter
        print('post action')


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
                'sales_year': 2018
            }

            self.header_list = [
                'sales season',
                'gross sales index',
                'gross sales',
                'AVT',
                'gross sales per unit',
                'discounts',
                'returns',
                'net sales',
                'sell through ratio',
                'sell in',
                'markup',
                'gross margin percentage',
                'gross margin',
                'buying budget',
                'GMROI % target',
                'beginning season inventory',
                'ending season inventory',
                'markdown',
            ]
            self.format_list = [
                'skip',
            	'input_key',
            	'input_intcomma_rounding0',
            	'intcomma_rounding0',
            	'intcomma_rounding0',
            	'intcomma_rounding0',
            	'input_intcomma_rounding0',
            	'input_intcomma_rounding0',
            	'intcomma_rounding0',
            	'input_intcomma_rounding0',
            	'intcomma_rounding0',
            	'input_percentagecomma',
            	'percentagemultiplied',
            	'intcomma_rounding0',
            	'intcomma_rounding0',
            	'percentagemultiplied',
            	'intcomma_rounding0',
            	'intcomma_rounding0',
            	'intcomma_rounding0',
            ]
            self.form_field_list = [
                'row_styling',
                'sales_season',
                'gross_sales_index',
                'gross_sales',
                'asp',
                'gross_sales_per_unit',
                'discounts',
                'returns',
                'net_sales',
                'sell_through_ratio',
                'sell_in',
                'markup',
                'gross_margin_percentage',
                'gross_margin',
                'buying_budget',
                'gmroi_percentage_target',
                'beginning_season_inventory',
                'ending_season_inventory',
                'markdown',
            ]
            self.tfoot = '2, 5, 6, 7'
            self.aggregation_dict = {
                # 'values': ['dim_channel', 'sales_year', 'sales_season', 'product_division'],
                'values': ['row_styling', 'sales_season'],
                'logic': {
                    'gross_sales_index_min': Min('gross_sales_index'),
                    'gross_sales_sum': Sum('gross_sales'),
                    'asp_sum': Sum('asp'),
                    'gross_sales_per_unit_sum': Sum('gross_sales_per_unit'),
                    'discounts_sum': Sum('discounts'),
                    'returns_sum': Sum('returns'),
                    'net_sales_sum': Sum('net_sales'),
                    'sell_through_ratio_min': Min('sell_through_ratio'),
                    'sell_in_sum': Sum('sell_in'),
                    'markup_sum': Sum('markup'),
                    'gross_margin_percentage_sum': Sum('gross_margin_percentage'),
                    'gross_margin_sum': Sum('gross_margin'),
                    'buying_budget_sum': Sum('buying_budget'),
                    'gmroi_percentage_target_sum': Sum('gmroi_percentage_target'),
                    'beginning_season_inventory_sum': Sum('beginning_season_inventory'),
                    'ending_season_inventory_sum': Sum('ending_season_inventory'),
                    'markdown_sum': Sum('markdown'),
                }
            }

        # sales_season
        elif self.xaxis == 'dim_channel__name':
            self.filter_dict = {
                'sales_year': 2018
            }

            self.header_list = [
                'channel',
                'gross sales index',
                'gross sales',
                'AVT',
                'gross sales per unit',
                'discounts',
                'returns',
                'net sales',
                'sell through ratio',
                'sell in',
                'markup',
                'gross margin percentage',
                'gross margin',
                'buying budget',
                'GMROI % target',
                'beginning season inventory',
                'ending season inventory',
                'markdown',
            ]
            self.format_list = [
                'skip',
            	'input_key',
            	'input_intcomma_rounding0',
            	'intcomma_rounding0',
            	'intcomma_rounding0',
            	'intcomma_rounding0',
            	'input_intcomma_rounding0',
            	'input_intcomma_rounding0',
            	'intcomma_rounding0',
            	'input_intcomma_rounding0',
            	'intcomma_rounding0',
            	'input_percentagecomma',
            	'percentagemultiplied',
            	'intcomma_rounding0',
            	'intcomma_rounding0',
            	'percentagemultiplied',
            	'intcomma_rounding0',
            	'intcomma_rounding0',
            	'intcomma_rounding0',
            ]
            self.form_field_list = [
                'row_styling',
                'dim_channel__name',
                'gross_sales_index',
                'gross_sales',
                'asp',
                'gross_sales_per_unit',
                'discounts',
                'returns',
                'net_sales',
                'sell_through_ratio',
                'sell_in',
                'markup',
                'gross_margin_percentage',
                'gross_margin',
                'buying_budget',
                'gmroi_percentage_target',
                'beginning_season_inventory',
                'ending_season_inventory',
                'markdown',
            ]
            self.tfoot = '2, 5, 6, 7'
            self.aggregation_dict = {
                # 'values': ['dim_channel', 'sales_year', 'sales_season', 'product_division'],
                'values': ['row_styling', 'dim_channel__name'],
                'logic': {
                    'gross_sales_index_min': Min('gross_sales_index'),
                    'gross_sales_sum': Sum('gross_sales'),
                    'asp_sum': Sum('asp'),
                    'gross_sales_per_unit_sum': Sum('gross_sales_per_unit'),
                    'discounts_sum': Sum('discounts'),
                    'returns_sum': Sum('returns'),
                    'net_sales_sum': Sum('net_sales'),
                    'sell_through_ratio_min': Min('sell_through_ratio'),
                    'sell_in_sum': Sum('sell_in'),
                    'markup_sum': Sum('markup'),
                    'gross_margin_percentage_sum': Sum('gross_margin_percentage'),
                    'gross_margin_sum': Sum('gross_margin'),
                    'buying_budget_sum': Sum('buying_budget'),
                    'gmroi_percentage_target_sum': Sum('gmroi_percentage_target'),
                    'beginning_season_inventory_sum': Sum('beginning_season_inventory'),
                    'ending_season_inventory_sum': Sum('ending_season_inventory'),
                    'markdown_sum': Sum('markdown'),
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
                'ASP',
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
                'asp',
                'average_cost_of_inventory',
                'intake_beginning_of_season',
            ]
            self.format_list = [
                'skip',
            	'input_key',
            	'input_key',
            	'input_intcomma_rounding0',
            	'intcomma_rounding0',
            	'input_intcomma_rounding0',
            	'input_intcomma_rounding0',
                'intcomma_rounding0',
            	'intcomma_rounding0',
                'input_intcomma_rounding0', # sell_through_ratio
            	'intcomma_rounding0', # sell_in
            	'intcomma_rounding0', # markup
            	'input_percentagecomma', # gross_margin_percentage
            	'intcomma_rounding0', # gross_magin_value
            	'intcomma_rounding0', # buying_budget
            	'percentagemultiplied', # gmroi_percentage_target
            	'intcomma_rounding0', # beginning_season_inventory
            	'intcomma_rounding0', # markdown
            	'intcomma_rounding0', # ending_season_inventory
            	'intcomma_rounding0', # asp
                'intcomma_rounding0', # average_cost_of_inventory
                'intcomma_rounding0', # intake_beginning_of_season
            ]
            self.tfoot = '3, 4, 5, 6, 7, 9'
            self.aggregation_dict = {
                'values': ['row_styling', 'sales_year', 'region'],
                'logic': {
                    'gross_sales_index_min': Min('gross_sales_index'), # input
                    'gross_sales_sum': Sum('gross_sales'),
                    'discounts_sum': Sum('discounts'), # input
                    'returns_sum': Sum('returns'), # input
                    'net_sales_sum': Sum('net_sales'),
                    'gross_sales_per_unit_sum': Sum('gross_sales_per_unit'),
                    'sell_through_ratio_min': Min('sell_through_ratio'), # input
                    'sell_in_sum': Sum('sell_in'),
                    'markup_sum': Sum('markup'), # input
                    'gross_margin_percentage_sum': Sum('gross_margin_percentage'),
                    'gross_margin_sum': Sum('gross_margin'),
                    'buying_budget_sum': Sum('buying_budget'),
                    'gmroi_percentage_target_sum': Sum('gmroi_percentage_target'),
                    'beginning_season_inventory_sum': Sum('beginning_season_inventory'),
                    'markdown_sum': Sum('markdown'),
                    'ending_season_inventory_sum': Sum('ending_season_inventory'),
                    'asp_sum': Sum('asp'),
                    'average_cost_of_inventory': Sum('average_cost_of_inventory'),
                    'intake_beginning_of_season': Sum('intake_beginning_of_season'),
                }
            }

    def post_action(self):
        # Prepare POST data
        # smart_save_input_dict = {
        #     'model': self.model._meta.db_table,
        #     'key_field': self.xaxis, # product_category
        #     'levels': ['dim_channel', 'sales_year', 'sales_season', 'region',],
        #     'field_reference': {
        #         'gross_sales_index': 'gross_sales',
        #         'discounts': 'discounts',
        #         'returns': 'returns',
        #         'sell_through_ratio': 'sell_through_ratio',
        #         'markup': 'markup',
        #     },
        #     'data': self.post_filter_dict
        # }
        # update_mix_index(smart_save_input_dict)

        # Additional calculations
        for item in self.model.objects.all():
            item.net_sales = item.gross_sales - item.discounts - item.returns
            item.gross_sales = item.gross_sales_init * item.gross_sales_index
            item.sell_in = item.net_sales * item.sell_through_ratio
            item.gross_margin_value = item.net_sales * item.gross_margin_percentage
            item.buying_budget = item.sell_in * item.markup
            item.beginning_season_inventory = 0
            item.ending_season_inventory = item.beginning_season_inventory - item.net_sales - item.markdown
            item.save()


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
