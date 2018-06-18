from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    # Search
    url(r'^search_api/$', views.SearchAPI.as_view(), name='search_api'),
    url(r'^search_api/(?P<query>[\w\-\s()]+)/$', views.SearchAPI.as_view(), name='search_api'),

    # Search results
    url(r'^product_attribute_table/(?P<pk>\d+)$', views.ProductAttributeTable.as_view(), name='product_attribute_table'),
    url(r'^vendor_attribute_table/(?P<pk>\d+)$', views.VendorAttributeTable.as_view(), name='vendor_attribute_table'),
    url(r'^demand_chart_api/(?P<aggregation>[\w]+)/$', views.DemandChartAPI.as_view(), name='demand_chart_api'),
    url(r'^demand_chart_api/(?P<aggregation>[\w]+)/(?P<category>[\w]+)/(?P<pk>\d+)$', views.DemandChartAPI.as_view(), name='demand_chart_api'),
    url(r'^demand_chart_api/(?P<aggregation>[\w]+)/(?P<category>[\w]+)/(?P<keyword>[\w\-\s()]+)$', views.DemandChartAPI.as_view(), name='demand_chart_api'),

    url(r'^search_result_product/(?P<keyword>.+)/$', views.SearchResultProduct.as_view(), name='search_result_product'),
    url(r'^search_result_vendor/(?P<keyword>.+)/$', views.SearchResultVendor.as_view(), name='search_result_vendor'),

    # Dashboard
    url(r'^latest_buy_demand_chart_api$', views.LatestBuyDemandChartAPI.as_view(), name='latest_buy_demand_chart_api'),
    url(r'^vfa_allocation_by_vendor_need_to_buy$', views.VFAAllocationByVendorNeedToBuy.as_view(), name='vfa_allocation_by_vendor_need_to_buy'),
    url(r'^vendor_map$', views.VendorMap.as_view(), name='vendor_map'),
    url(r'^vendor_map/(?P<pk>\d+)$', views.VendorMap.as_view(), name='vendor_map'),
    url(r'^vendor_map_api$', views.VendorMapAPI.as_view(), name='vendor_map_api'),
    url(r'^vendor_map_api/(?P<pk>\d+)$', views.VendorMapAPI.as_view(), name='vendor_map_api'),
    url(r'^vfa_allocation_map$', views.VFAAllocationMap.as_view(), name='vfa_allocation_map'),
    url(r'^vfa_allocation_map_api$', views.VFAAllocationMapAPI.as_view(), name='vfa_allocation_map_api'),

    # Reports
    url(r'^monthly_buy_by_region$', views.MonthlyBuyByRegion.as_view(), name='monthly_buy_by_region'),
    url(r'^monthly_buy_pivottable$', views.MonthlyBuyPivotTable.as_view(), name='monthly_buy_pivottable'),
    url(r'^shipment_status_vendor_pivottable$', views.ShipmentStatusByVendorPivotTable.as_view(), name='shipment_status_vendor_pivottable'),
    url(r'^shipment_status_region_pivottable$', views.ShipmentStatusByRegionPivotTable.as_view(), name='shipment_status_region_pivottable'),

    # handsontable
    url(r'^handsontable/(?P<item>[\w]+)/$', views.MasterTableAPI.as_view(), name='handsontable'), # For DRF page
    url(r'^handsontable_header/(?P<item>[\w]+)/$', views.MasterTableHeaderAPI.as_view(), name='handsontable_header'), # For DRF page

    # tokenfield
    url(r'^tokenfield_dimproduct_material_id$', views.TokenFieldDimProductMaterialId.as_view(), name='tokenfield_dimproduct_material_id'),
    url(r'^tokenfield_dimproduct_material_id_emea$', views.TokenFieldDimProductMaterialIdEmea.as_view(), name='tokenfield_dimproduct_material_id_emea'),
    url(r'^tokenfield_order_number$', views.TokenFieldOrderNumber.as_view(), name='tokenfield_order_number'),

    # RPC
    url(r'^procedure_run/(?P<item>[\w]+)/$', views.StoredProcedureAPI.as_view(), name='procedure_run'), # For DRF page

    # Core
    url(r'^procedure_list$', views.StoredProcedureList.as_view(), name='procedure_list'),
    url(r'^configuration_table$', views.ConfigurationTable.as_view(), name='configuration_table'),
    url(r'^validation_table$', views.ValidationReportTable.as_view(), name='validation_table'),
    url(r'^pdas_metadata_table$', views.SourceExtractTable.as_view(), name='pdas_metadata_table'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
