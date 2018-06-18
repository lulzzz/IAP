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

from workflows.execution.vans_pdas import calls


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
                'search_tab': 'search_tab_multiple_product', # only for multiple
                'model': models.DimProduct,
                'search_field_label': 'MAT #',
                'search_field': 'material_id',
                'search_type': 'icontains',
                'additional_filter': {'is_placeholder': False},
                'is_unique': False,
            },
            {
                'search_tab': 'search_tab_multiple_product', # only for multiple
                'model': models.DimProduct,
                'search_field_label': 'style',
                'search_field': 'style_name',
                'search_type': 'icontains',
                'additional_filter': {'is_placeholder': False},
                'is_unique': False,
            },
            {
                'search_tab': 'search_tab_multiple_product', # only for multiple
                'model': models.DimProduct,
                'search_field_label': 'style complexity',
                'search_field': 'style_complexity',
                'search_type': 'icontains',
                'additional_filter': {'is_placeholder': False},
                'is_unique': False,
            },
            # {
            #     'search_tab': 'search_tab_multiple_product', # only for multiple
            #     'model': models.DimCustomer,
            #     'search_field_label': 'customer',
            #     'search_field': 'name',
            #     'search_type': 'icontains',
            #     'is_unique': False,
            # },
            {
                'search_tab': 'search_tab_multiple_product', # only for multiple
                'model': models.DimCustomer,
                'search_field_label': 'customer',
                'search_field': 'name',
                'search_type': 'icontains',
                'additional_filter': {'is_placeholder': False},
                'is_unique': False,
            },
            {
                'search_tab': 'search_tab_one_vendor', # only for multiple
                'model': models.DimFactory,
                'search_field_label': 'factory code',
                'search_field': 'short_name',
                'search_type': 'icontains',
                'additional_filter': {'is_placeholder': False},
                'is_unique': True,
            },
            {
                'search_tab': 'search_tab_multiple_vendor', # only for multiple
                'model': models.DimLocation,
                'search_field_label': 'factory country',
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


class ConfigurationTable(views.FormValidation):
    r"""
    View that shows/updates the PDAS release configuration table
    """
    model = models.HelperPdasFootwearVansReleaseCurrent
    form_class = forms.HelperPdasFootwearVansReleaseCurrentForm
    pk = 1


class ValidationReportTable(views.TableRead):
    r"""
    View that shows the content of system_log_file (validation of source files)
    """

    model = models.SystemLogFile
    format_list = [None, None, None,]


class SourceExtractTable(views.TableRead):
    r"""
    View that shows the content of pdas_metadata (latest extracts)
    """

    model = models.PdasMetadata
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
    format_list = ['link', None, None, None, None, None,]
    form_field_list = [
        'link',
        'material_id',
        'size',
        'style_name',
        'style_complexity',
        [
            'dim_construction_type',
            [
                'name',
            ],
        ],
    ]

    def set_filter_dict(self):
        query = (Q(is_placeholder=False) & \
            (
                Q(material_id=self.keyword) |
                Q(style_name=self.keyword) |
                Q(color_description=self.keyword) |
                Q(gender_new=self.keyword) |
                Q(color_description=self.keyword) |
                Q(style_complexity=self.keyword) |
                Q(dim_construction_type__name=self.keyword)
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
        'short_name',
        'vendor_group',
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
                Q(dim_location__country=self.keyword)
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

        # Query images
        query = models.DimProductImageAssociation.objects.filter(
            dim_product__id=self.pk
        ).all()

        image_list = list()
        for image in query:
            image_list.append({
                'label': image.category,
                'reference': image.relative_path,
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


class VFAAllocationMap(project_mixins_view.ReleaseFilter, views.WorldMap):
    r"""
    View that shows the allocated product counts on a worldmap (map structure)
    """

    def get_context_dict(self, request):
        # Extend filter
        self.filter_dict['dim_date_id__gte'] = self.dim_release_dim_date_id

        label_list = sorted(list(set(models.FactDemandTotal.objects.filter(**self.filter_dict).values_list('dim_factory__dim_location__country', flat=True))), key=str.lower)
        data_list = list()
        total = 0

        temp_filter_dict = self.filter_dict
        for label in label_list:
            temp_filter_dict['dim_factory__dim_location__country'] = label
            label_count = models.FactDemandTotal.objects.filter(**temp_filter_dict).aggregate(Sum('quantity_lum')).get('quantity_lum__sum')
            total += label_count
            data_list.append({
                'label': label,
                'value': '{:,}'.format(label_count),
            })

        return {
            'height': '280',
            'title': 'Buy Volume',
            'total': '{:,}'.format(total),
            'table_items': data_list
        }


class VFAAllocationMapAPI(project_mixins_view.ReleaseFilter, views.WorldMap):
    r"""
    View that shows the allocated product counts on a worldmap (data)
    """

    def get(self, request, format=None, **kwargs):
        # Extend filter
        self.filter_dict['dim_date_id__gte'] = self.dim_release_dim_date_id

        label_list = sorted(list(set(models.FactDemandTotal.objects.filter(**self.filter_dict).values_list('dim_factory__dim_location__country_code_a2', flat=True))), key=str.lower)
        label_list = [x.lower() for x in label_list]
        data_dict = dict()
        temp_filter_dict = self.filter_dict
        for label in label_list:
            temp_filter_dict['dim_factory__dim_location__country_code_a2__iexact'] = label
            data_dict[label] = '1'

        return JsonResponse(data_dict, safe=False)


class DemandChartAPI(project_mixins_view.ReleaseFilter, views.ChartAPI):
    r'''
    View that provides the chart configuration and data
    '''
    # Variable definition
    model = models.FactDemandTotal
    order_by = 'dim_date__year_month_accounting'
    xaxis = 'dim_date__year_month_accounting'
    chart_label = 'Volume'
    aggregation = 'quantity_lum'
    aggregation_label = 'quantity LUM'
    filter_dict = None

    def set_filter_dict(self):
        # vendor
        if self.kwargs.get('category') == 'dim_factory_final':
            # pk
            if self.kwargs.get('pk'):
                self.filter_dict['dim_factory_id_final__exact'] = self.kwargs.get('pk')
            # keyword
            elif self.kwargs.get('keyword'):
                pass

        # product
        elif self.kwargs.get('category') == 'dim_product':
            # pk
            if self.kwargs.get('pk'):
                self.filter_dict['dim_product_id__exact'] = self.kwargs.get('pk')
            # keyword
            elif self.kwargs.get('keyword'):
                query = (Q(dim_product__is_placeholder=False) & \
                    (
                        Q(dim_product__material_id=self.kwargs.get('keyword')) |
                        Q(dim_product__style_name=self.kwargs.get('keyword')) |
                        Q(dim_product__color_description=self.kwargs.get('keyword')) |
                        Q(dim_product__gender_new=self.kwargs.get('keyword')) |
                        Q(dim_product__color_description=self.kwargs.get('keyword')) |
                        Q(dim_product__style_complexity=self.kwargs.get('keyword')) |
                        Q(dim_product__dim_construction_type__name=self.kwargs.get('keyword'))
                    )
                )
                self.filter_dict = query

        # no selection
        else:
            self.filter_dict['dim_date_id__gte'] = self.dim_release_dim_date_id


class LatestBuyDemandChartAPI(project_mixins_view.ReleaseFilter, views.ChartAPI):
    r'''
    View that provides the chart configuration and data
    '''
    # Variable definition
    model = models.FactDemandTotal
    order_by = 'dim_factory__vendor_group'
    xaxis = 'dim_factory__vendor_group'
    chart_label = 'Volume'
    aggregation = 'quantity_lum'
    aggregation_label = 'quantity LUM'
    filter_dict = None

    def get(self, request, format=None, **kwargs):
        # Prepare filter
        self.filter_dict['dim_date_id__gte'] = self.dim_release_dim_date_id

        # Base queryset
        queryset = self.model.objects.filter(**self.filter_dict)

        # Prepare labels
        label_list = sorted(list(set(queryset.values_list(self.xaxis, flat=True))))

        # Prepare lists
        data_list_nora = [0] * len(label_list)
        data_list_emea = [0] * len(label_list)
        data_list_casa = [0] * len(label_list)
        data_list_apac = [0] * len(label_list)

        # Load data for each region
        for label in label_list:
            data_list_query = queryset.filter(**{self.xaxis:label}).values(
                'dim_customer__dim_location__region'
            ).annotate(
                aggregation_sum=Sum(self.aggregation)
            ).order_by(self.xaxis)

            for data_dict in list(data_list_query):
                if data_dict.get('dim_customer__dim_location__region') == 'NORA':
                    data_list_nora[label_list.index(label)] = data_dict.get('aggregation_sum')
                if data_dict.get('dim_customer__dim_location__region') == 'EMEA':
                    data_list_emea[label_list.index(label)] = data_dict.get('aggregation_sum')
                if data_dict.get('dim_customer__dim_location__region') == 'CASA':
                    data_list_casa[label_list.index(label)] = data_dict.get('aggregation_sum')
                if data_dict.get('dim_customer__dim_location__region') == 'APAC':
                    data_list_apac[label_list.index(label)] = data_dict.get('aggregation_sum')

        data = {
            'labels': label_list,
            'datasets': [
                {
                    'label': 'NORA',
                    'data': data_list_nora,
                    'backgroundColor': ['#a5d127' for x in list(range(len(label_list)))],
                    'borderColor': ['#a5d127' for x in list(range(len(label_list)))],
                    'borderWidth': 2
                },
                {
                    'label': 'EMEA',
                    'data': data_list_emea,
                    'backgroundColor': ['#519bc4' for x in list(range(len(label_list)))],
                    'borderColor': ['#519bc4' for x in list(range(len(label_list)))],
                    'borderWidth': 2
                },
                {
                    'label': 'CASA',
                    'data': data_list_casa,
                    'backgroundColor': ['#b58c89' for x in list(range(len(label_list)))],
                    'borderColor': ['#b58c89' for x in list(range(len(label_list)))],
                    'borderWidth': 2
                },
                {
                    'label': 'APAC',
                    'data': data_list_apac,
                    'backgroundColor': ['#c45850' for x in list(range(len(label_list)))],
                    'borderColor': ['#c45850' for x in list(range(len(label_list)))],
                    'borderWidth': 2
                },
            ]
        }

        return JsonResponse(data, safe=False)


class VFAAllocationByVendorNeedToBuy(project_mixins_view.ReleaseFilter, views.TableRead):
    r"""
    View that shows the content of the table (aggregated by vendor)
    """

    model = models.FactDemandTotal
    header_list = ['factory', 'region', 'MTL count', 'MTL-size count', 'quantity LUM']
    aggregation_dict = {
        'values': ['dim_factory__short_name', 'dim_customer__dim_location__region'],
        'logic': {
            'dim_product__material_id_count': Count('dim_product__material_id', distinct = True),
            'dim_product_id_count': Count('dim_product_id', distinct = True),
            'quantity_lum_sum': Sum('quantity_lum'),
        }
    }
    order_by = 'dim_factory__short_name'
    format_list = [None, None, 'intcomma_rounding0', 'intcomma_rounding0', 'intcomma_rounding0']
    tfoot = '4'

    def set_filter_dict(self):
        # Extend filter
        pass


class MonthlyBuyByRegion(views.TableRead):
    r"""
    View that shows the content of the table (aggregated by region)
    """

    model = models.FactDemandTotal
    header_list = ['region', 'buy month', 'quantity LUM']
    aggregation_dict = {
        'values': [
            'dim_customer__dim_location__region',
            'dim_date_id_buy_month__year_month_accounting'
        ],
        'logic': {
            'quantity_lum_sum': Sum('quantity_lum'),
        }
    }
    order_by = 'dim_factory__short_name'
    format_list = [None, None, 'intcomma_rounding0']
    tfoot = '2'

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
        self.filter_dict['dim_demand_category__name'] = 'Need to Buy'


class MonthlyBuyPivotTable(views.PivotTableAPI):
    r"""
    View that shows the content of the pivot table
    """

    model = models.FactDemandTotal
    header_dict = {
        'dim_product__style_complexity': 'style complexity',
        'dim_product__gender_new': 'gender',
        'dim_product__style_name': 'description',
        'dim_product__color_description': 'color',
        'dim_product__material_id': 'MTL #',
        'dim_customer__dim_location__region': 'region',
        'dim_buying_program__name': 'buying program',
        'dim_date_id_buy_month__year_month_accounting': 'CRD month',
        'dim_factory__short_name': 'vendor',
        'quantity_lum_sum': 'quantity LUM',
        'quantity': 'quantity',
    }
    aggregation_dict = {
        'values': [
            'dim_product__style_complexity',
            'dim_product__gender_new',
            'dim_product__style_name',
            'dim_product__color_description',
            'dim_product__material_id',
            'dim_customer__dim_location__region',
            'dim_buying_program__name',
            'dim_date_id_buy_month__year_month_accounting',
            'dim_factory__short_name',
        ],
        'logic': {
            'quantity_lum_sum': Sum('quantity_lum'),
            'quantity': Sum('quantity_lum'),
        }
    }

    def set_filter_dict(self):
        self.filter_dict['dim_demand_category__name'] = 'Need to Buy'

    # Return empty json with GET
    def get(self, request, format=None, **kwargs):
        return JsonResponse([], safe=False)


class ShipmentStatusByVendorPivotTable(project_mixins_view.ReleaseFilter, views.PivotTableAPI):
    r"""
    View that shows the content of the pivot table
    """

    model = models.FactDemandTotal
    header_dict = {
        'dim_product__style_complexity': 'style complexity',
        'dim_product__gender_new': 'gender',
        'dim_product__style_name': 'description',
        'dim_product__color_description': 'color',
        'dim_product__material_id': 'MTL #',
        'dim_product__material_id_emea': 'MTL # (EMEA)',
        'dim_factory__short_name': 'vendor',
        'dim_demand_category__name': 'demand signal type',
        'dim_date__year_month_accounting': 'CRD month',
        'quantity_lum_sum': 'quantity LUM',
        'quantity': 'quantity',
    }
    aggregation_dict = {
        'values': [
            'dim_product__style_complexity',
            'dim_product__gender_new',
            'dim_product__style_name',
            'dim_product__color_description',
            'dim_product__material_id',
            'dim_product__material_id_emea',
            'dim_factory__short_name',
            'dim_demand_category__name',
            'dim_date__year_month_accounting',
        ],
        'logic': {
            'quantity_lum_sum': Sum('quantity_lum'),
            'quantity': Sum('quantity_lum'),
        }
    }

    # Return empty json with GET
    def get(self, request, format=None, **kwargs):
        return JsonResponse([], safe=False)


class ShipmentStatusByRegionPivotTable(project_mixins_view.ReleaseFilter, views.PivotTableAPI):
    r"""
    View that shows the content of the pivot table
    """

    model = models.FactDemandTotal
    header_dict = {
        'dim_product__style_complexity': 'style complexity',
        'dim_product__gender_new': 'gender',
        'dim_product__style_name': 'description',
        'dim_product__color_description': 'color',
        'dim_product__material_id': 'MTL #',
        'dim_product__material_id_emea': 'MTL # (EMEA)',
        'dim_factory__short_name': 'vendor',
        'dim_customer__dim_location__region': 'region',
        'dim_demand_category__name': 'demand signal type',
        'dim_date__year_month_accounting': 'CRD month',
        'quantity_lum_sum': 'quantity LUM',
        'quantity': 'quantity',
    }
    aggregation_dict = {
        'values': [
            'dim_product__style_complexity',
            'dim_product__gender_new',
            'dim_product__style_name',
            'dim_product__color_description',
            'dim_product__material_id',
            'dim_product__material_id_emea',
            'dim_factory__short_name',
            'dim_customer__dim_location__region',
            'dim_demand_category__name',
            'dim_date__year_month_accounting',
        ],
        'logic': {
            'quantity_lum_sum': Sum('quantity_lum'),
            'quantity': Sum('quantity_lum'),
        }
    }

    # Return empty json with GET
    def get(self, request, format=None, **kwargs):
        return JsonResponse([], safe=False)


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
    model = models.FactDemandTotal
    field_name = 'order_number'
