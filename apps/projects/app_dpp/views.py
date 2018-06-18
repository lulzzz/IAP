import json

from django.conf import settings as cp
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError
from django.urls import reverse_lazy
from django.db.models import Count, Sum, Case, When, Value, IntegerField
from django.db.models import Q
from django.db.models.functions import Lower, Upper

from rest_framework import status # To return status codes
from rest_framework.views import APIView
from rest_framework.response import Response

from core import gcbvs
from core import utils
from core import mixins_view
from blocks import views

from apps.standards.app_console import mixins_apiview
from apps.standards.app_console.models import UserPermissions
from apps.standards.app_console.models import GroupPermissions
from apps.standards.app_console.models import Item

from . import models
from . import forms
from . import serializers
from . import mixins_view as project_mixins_view

# from workflows.execution.bauer_dpp import calls


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
            'model': models.DimProduct,
            'search_field_label': 'SKU',
            'search_field': 'sku',
            'search_type': 'icontains',
            'additional_filter': {'is_placeholder': False},
            'is_unique': True,
        },
            {
                'search_tab': 'search_tab_multiple_product', # only for multiple
                'model': models.DimProduct,
                'search_field_label': 'material description',
                'search_field': 'material_description',
                'search_type': 'icontains',
                'additional_filter': {'is_placeholder': False},
                'is_unique': False,
            },
            {
                'search_tab': 'search_tab_multiple_product', # only for multiple
                'model': models.DimProduct,
                'search_field_label': 'PGS',
                'search_field': 'pgs',
                'search_type': 'icontains',
                'additional_filter': {'is_placeholder': False},
                'is_unique': False,
            },
            {
                'search_tab': 'search_tab_multiple_product', # only for multiple
                'model': models.DimProduct,
                'search_field_label': 'gender',
                'search_field': 'gender_label',
                'search_type': 'icontains',
                'additional_filter': {'is_placeholder': False},
                'is_unique': False,
            },
            {
                'search_tab': 'search_tab_one_vendor', # only for multiple
                'model': models.DimFactory,
                'search_field_label': 'plant code',
                'search_field': 'plant_code',
                'search_type': 'icontains',
                'additional_filter': {'is_placeholder': False},
                'is_unique': True,
            },
            {
                'search_tab': 'search_tab_multiple_vendor', # only for multiple
                'model': models.DimFactory,
                'search_field_label': 'vendor name',
                'search_field': 'vendor_name',
                'search_type': 'icontains',
                'additional_filter': {'is_placeholder': False},
                'is_unique': False,
            },
            {
                'search_tab': 'search_tab_multiple_vendor', # only for multiple
                'model': models.DimLocation,
                'search_field_label': 'plant country',
                'search_field': 'country',
                'search_type': 'icontains',
                'is_unique': False,
            },
        ]
        serializer_combined = utils.generate_search_list(query, query_list_of_dict)

        return JsonResponse(serializer_combined, safe=False)


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
    View that loads the table header.
    Assuming user group has required permissions.
    """

    def get_model_obj(self):
        return eval('models.' + self.model_name)

    def get_serializer_obj(self):
        return eval('serializers.' + self.model_name + 'Serializer')


class StoredProcedureAPI(mixins_apiview.StoredProcedureAPI):
    r"""
    View that runs the RPC
    """

    def get_model_obj(self, param):
        return getattr(calls, param)()


class StoredProcedureList(views.TableProcedure, mixins_view.SecurityModelNameMixin):
    r"""
    View that shows the Console stored procedures that a user can run
    """

    user_permission_model = UserPermissions
    group_permission_model = GroupPermissions
    target_model = Item
    permission_type = ['rpc']

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


class ValidationReportTable(views.TableRead):
    r"""
    View that shows the content of system_log_file (validation of source files)
    """

    model = models.SystemLogFile
    format_list = [None, None, None,]


class SourceExtractTable(views.TableRead):
    r"""
    View that shows the content of metadata (latest extracts)
    """

    model = models.SourceMetadata
    order_by = '-timestamp_file'
    is_datatable = False
    js_list = []
    format_list = [None, 'datetime',]


class SearchResultProduct(views.TableRead):
    r"""
    View that shows the content of the table
    """

    model = models.DimProduct
    limit = 500
    format_list = ['link', None, None, None, None,]
    header_list = ['link', 'SKU', 'material description', 'PGS', 'gender']
    form_field_list = [
        'link',
        'sku',
        'material_description',
        'pgs',
        'gender_label',
    ]

    def set_filter_dict(self):
        query = (Q(is_placeholder=False) & \
            (
                Q(material_description=self.keyword) |
                Q(pgs=self.keyword) |
                Q(gender_label=self.keyword)
            )
        )

        self.filter_dict = query


class SearchResultVendor(views.TableRead):
    r"""
    View that shows the content of the table
    """

    model = models.DimFactory
    limit = 500
    format_list = ['link', None, None, 'boolean', None, None, 'boolean', 'boolean']
    form_field_list = [
        'link',
        'plant_code',
        'vendor_name',
        'vendor_code',
        'is_active',
        [
            'dim_location',
            [
                'country',
                'region',
            ],
        ],
    ]

    def set_filter_dict(self):
        query = (Q(is_placeholder=False) & \
            (
                Q(dim_location__country=self.keyword) |
                Q(vendor_name=self.keyword)
            )
        )

        self.filter_dict = query


class ProductAttributeTable(views.FormValidation):
    r"""
    View that shows/updates the product table
    """
    # Define variables
    form_class = forms.ProductForm
    model = models.DimProduct


class VendorAttributeTable(views.FormValidation):
    r"""
    View that shows/updates the product table
    """
    form_class = forms.VendorForm
    model = models.DimFactory



class ProductImageGallery(views.MediaGallery):
    r"""
    View that shows the product images
    """

    def get_context_dict(self, request):
        image_list = list()
        image_list.append({
            'label': 'Sample',
            'full_row': True,
            'reference': '/products/bauer-hockey-skates-vapor-x800-jr.jpg',
        })

        return image_list


class VendorMap(project_mixins_view.ReleaseFilter, views.WorldMap):
    r"""
    View that shows the vendors counts on a worldmap (map structure)
    """

    def get_context_dict(self, request):

        if self.kwargs.get('pk'):
            return {'height': '300'}

        label_list = sorted(list(set(models.DimFactory.objects.values_list('dim_location__country_code_a2', flat=True))), key=str.lower)
        data_list = list()
        total = 0
        for label in label_list:
            label_count = models.DimFactory.objects.filter(dim_location__country=label).count()
            total += label_count
            data_list.append({
                'label': label,
                'value': '{:,}'.format(label_count),
            })

        return {
            'height': '300',
            'title': 'Number of vendors',
            'total': '{:,}'.format(total),
            'table_items': data_list
        }


class VendorMapAPI(project_mixins_view.ReleaseFilter, views.WorldMap):
    r"""
    View that shows the vendors counts on a worldmap (data)
    """

    def get(self, request, format=None, **kwargs):

        if self.kwargs.get('pk'):
            model_obj = models.DimFactory.objects.filter(pk=self.kwargs.get('pk')).get()
            country = model_obj.dim_location.country_code_a2.lower()
            label_list = [country]
            data_dict = dict()
            data_dict[country] = str(1)
        else:
            label_list = sorted(list(set(models.DimFactory.objects.values_list('dim_location__country_code_a2', flat=True))), key=str.lower)
            label_list = [x.lower() for x in label_list]
            data_dict = dict()
            for label in label_list:
                data_dict[label] = str(models.DimFactory.objects.filter(dim_location__country_code_a2=label).count())

        return JsonResponse(data_dict, safe=False)


class DemandChartAPI(project_mixins_view.ReleaseFilter, views.ChartAPI):
    r'''
    View that provides the chart configuration and data
    '''
    # Variable definition
    model = models.FactDemand
    order_by = 'dim_date_month_xf__year_month'
    xaxis = 'dim_date_month_xf__year_month'
    chart_label = 'Volume'
    aggregation = 'quantity'
    aggregation_label = 'quantity'
    filter_dict = None

    def set_filter_dict(self):
        # vendor
        if self.kwargs.get('category') == 'dim_production_line':
            # pk
            if self.kwargs.get('pk'):
                self.filter_dict['dim_production_line__exact'] = self.kwargs.get('pk')

        # product
        elif self.kwargs.get('category') == 'dim_product':
            # pk
            if self.kwargs.get('pk'):
                self.filter_dict['dim_product_id__exact'] = self.kwargs.get('pk')
            # keyword
            elif self.kwargs.get('keyword'):
                query = (Q(dim_product__is_placeholder=False) & \
                    (
                        Q(dim_product__material=self.kwargs.get('keyword')) |
                        Q(dim_product__material_text_short=self.kwargs.get('keyword')) |
                        Q(dim_product__family=self.kwargs.get('keyword')) |
                        Q(dim_product__group_description=self.kwargs.get('keyword'))
                    )
                )
                self.filter_dict = query


class DemandComboChartAPI(project_mixins_view.ReleaseFilter, views.ChartAPI):
    r'''
    View that provides the chart configuration and data
    '''
    # Variable definition
    model = models.FactDemand
    order_by = 'dim_date_month_xf__year_month'
    aggregation = 'quantity'
    aggregation_label = 'quantity'
    aggregation_dict = {
        'values': ['dim_demand_category__name', 'dim_date_month_xf__year_month',],
        'logic': {
            'units_sum': Sum('quantity'),
        }
    }
    filter_dict = None

    def return_value_or_zero(self, queryset_dict):
        if queryset_dict.get('quantity__sum'):
            return queryset_dict.get('quantity__sum')
        return 0


    def get(self, request, format=None, **kwargs):

        # Set filter_dict
        self.set_filter_dict()
        label_list = sorted(list(set(models.FactDemand.objects.filter(**self.filter_dict).values_list('dim_date_month_xf__year_month', flat=True))), key=str.lower)
        data_dict_direct_ship = ['Direct Ship']
        data_dict_warehouse_replenishment = ['Warehouse Replenishment']
        data_dict_forecast = ['Forecast']
        data_dict_capacity = ['Capacity']

        for label in label_list:
            xf_month_filter_dict = self.filter_dict.copy()
            xf_month_filter_dict['dim_date_month_xf__year_month'] = label
            fact_demand = models.FactDemand.objects
            fact_capacity = models.FactCapacity.objects.filter(**xf_month_filter_dict)

            data_dict_direct_ship.append(self.return_value_or_zero(fact_demand.filter(
                **xf_month_filter_dict,
                **{'dim_demand_category__name': 'Direct Ship'}
            ).aggregate(Sum('quantity'))))
            data_dict_warehouse_replenishment.append(self.return_value_or_zero(fact_demand.filter(
                **xf_month_filter_dict,
                **{'dim_demand_category__name': 'Warehouse Replenishment'}
            ).aggregate(Sum('quantity'))))
            data_dict_forecast.append(self.return_value_or_zero(fact_demand.filter(
                **xf_month_filter_dict,
                **{'dim_demand_category__name': 'Forecast'}
            ).aggregate(Sum('quantity'))))
            data_dict_capacity.append(self.return_value_or_zero(fact_capacity.aggregate(Sum('quantity'))))

        data_dict = {
            'bindto': '.combochartjs',
            'data': {
                'columns': [
                    data_dict_direct_ship,
                    data_dict_warehouse_replenishment,
                    data_dict_forecast,
                    data_dict_capacity,
                ],
                'type': 'bar',
                'types': {
                    'Capacity': 'spline',
                },
                'groups': [
                    [data_dict_direct_ship[0], data_dict_warehouse_replenishment[0], data_dict_forecast[0]]
                ],
                'colors': {
                    'Direct Ship': '#254e93',
                    'Warehouse Replenishment': '#7fc97f',
                    'Forecast': '#c11e1e',
                    'Capacity': '#252126',
                },
            },
            'axis': {
                'x': {
                    'type': 'category',
                    'categories': label_list
                }
            }
        }

        return JsonResponse(data_dict, safe=False)


    def set_filter_dict(self):
        # vendor
        if self.kwargs.get('category') == 'dim_production_line':
            # pk
            if self.kwargs.get('pk'):
                self.filter_dict['dim_production_line__exact'] = self.kwargs.get('pk')

        # product
        elif self.kwargs.get('category') == 'dim_product':
            # pk
            if self.kwargs.get('pk'):
                self.filter_dict['dim_product_id__exact'] = self.kwargs.get('pk')
            # keyword
            elif self.kwargs.get('keyword'):
                query = (Q(dim_product__is_placeholder=False) & \
                    (
                        Q(dim_product__material=self.kwargs.get('keyword')) |
                        Q(dim_product__material_text_short=self.kwargs.get('keyword')) |
                        Q(dim_product__family=self.kwargs.get('keyword')) |
                        Q(dim_product__group_description=self.kwargs.get('keyword'))
                    )
                )
                self.filter_dict = query


class ScenarioComparisonPivotTable(project_mixins_view.ReleaseFilter, views.PivotTableAPI):
    r"""
    View that shows the content of the pivot table
    """

    model = models.FactDemandAllocation
    header_dict = {
        'dim_demand_category__name': 'demand signal type',
        'dim_product__family': 'family',
        'dim_product__material': 'material',
        'dim_product__dim_construction_type__name': 'construction type',
        'allocation_logic': 'logic',
        'dim_scenario__name': 'scenario',
        'dim_production_line__line': 'production line',
        'dim_date_month_xf_user__year_month': 'XF month (user)',
        'quantity_user_sum': 'quantity (user)',
    }
    aggregation_dict = {
        'values': [
            'dim_demand_category__name',
            'dim_product__family',
            'dim_product__material',
            'dim_product__dim_construction_type__name',
            'allocation_logic',
            'dim_scenario__name',
            'dim_production_line__line',
            'dim_date_month_xf_user__year_month',
        ],
        'logic': {
            'quantity_user_sum': Sum('quantity_user'),
        }
    }

    # Return empty json with GET
    # def get(self, request, format=None, **kwargs):
    #     return JsonResponse([], safe=False)



class ConfigurationTable(views.FormValidation):
    r"""
    View that shows/updates the release configuration table
    """
    model = models.HelperReleaseCurrent
    form_class = forms.HelperReleaseCurrentForm
    pk = 1


class TokenFieldDimProductMaterialId(views.TokenFieldAPI):
    r"""
    View that loads the data for tokenfield.
    """
    model = models.DimProduct
    field_name = 'material_id'

class TokenFieldDimProductMaterialIdEmea(views.TokenFieldAPI):
    r"""
    View that loads the data for tokenfield.
    """
    model = models.DimProduct
    field_name = 'material_id_emea'

class TokenFieldOrderNumber(project_mixins_view.ReleaseFilter, views.TokenFieldAPI):
    r"""
    View that loads the data for tokenfield.
    """
    model = models.FactDemand
    field_name = 'order_number'



class ScenarioConfiguration(views.FormValidation):
    r"""
    View that shows/updates the product table
    """
    # Define variables
    form_class = forms.ProductSelectedTrueForm
    model = models.DimProduct



class DecisionTree(project_mixins_view.ReleaseFilter, views.TreeView):
    r"""
    View that loads the decision trees.
    """

    def get_context_dict(self, request):

        scenario = {
            # Check which type of demand
            'condition': 'Demand Category',
            'branches': {
                'Direct Ship': {
                    'condition': 'Product Group',
                    'branches': {
                        'Skates': {
                            'condition': 'Segment',
                            'branches': {
                                'Elite': 'Constrained'
                            }
                        }
                    }
                },
                'Warehouse Replenishment': {
                    'condition': 'Product Group',
                    'branches': {
                        'Skates': {
                            'condition': 'Segment',
                            'branches': {
                                'Elite': 'Constrained'
                            }
                        }
                    }
                },
                'Forecast': {
                    'condition': 'Product Group',
                    'branches': {
                        'Skates': {
                            'condition': 'Segment',
                            'branches': {
                                'Elite': 'Constrained'
                            }
                        }
                    }
                }
            }
        }

        return scenario
