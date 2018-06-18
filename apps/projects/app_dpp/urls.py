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

    url(r'^product_image_gallery$', views.ProductImageGallery.as_view(), name='product_image_gallery'),
    url(r'^product_image_gallery/(?P<pk>\d+)$', views.ProductImageGallery.as_view(), name='product_image_gallery'),

    url(r'^search_result_product/(?P<keyword>.+)/$', views.SearchResultProduct.as_view(), name='search_result_product'),
    url(r'^search_result_vendor/(?P<keyword>.+)/$', views.SearchResultVendor.as_view(), name='search_result_vendor'),

    # Dashboard
    url(r'^latest_demand_chart_api$', views.DemandChartAPI.as_view(), name='latest_demand_chart_api'),
    url(r'^latest_demand_combochart_api$', views.DemandComboChartAPI.as_view(), name='latest_demand_combochart_api'),

    # handsontable
    url(r'^handsontable/(?P<item>[\w]+)/$', views.MasterTableAPI.as_view(), name='handsontable'), # For DRF page
    url(r'^handsontable_header/(?P<item>[\w]+)/$', views.MasterTableHeaderAPI.as_view(), name='handsontable_header'), # For DRF page

    # pivot table
    url(r'^scenario_pivottable$', views.ScenarioComparisonPivotTable.as_view(), name='scenario_pivottable'),

    # tokenfield
    url(r'^tokenfield_order_number$', views.TokenFieldOrderNumber.as_view(), name='tokenfield_order_number'),

    # RPC
    url(r'^procedure_run/(?P<item>[\w]+)/$', views.StoredProcedureAPI.as_view(), name='procedure_run'), # For DRF page

    # Core
    url(r'^procedure_list$', views.StoredProcedureList.as_view(), name='procedure_list'),
    url(r'^configuration_table$', views.ConfigurationTable.as_view(), name='configuration_table'),
    url(r'^validation_table$', views.ValidationReportTable.as_view(), name='validation_table'),
    url(r'^source_metadata_table$', views.SourceExtractTable.as_view(), name='source_metadata_table'),

    # Scenario
    url(r'^scenario_configuration$', views.ScenarioConfiguration.as_view(), name='scenario_configuration'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
