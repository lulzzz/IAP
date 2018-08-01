from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    url(r'^search_api/$', views.SearchAPI.as_view(), name='search_api'), # For user search
    url(r'^search_api/(?P<keyword>[\w]+)/(?P<query>[\w\-\s()]+)/$', views.SearchAPI.as_view(), name='search_api'), # For DRF page

    # Search single
    url(r'^product_attribute_table/(?P<pk>\d+)$', views.ProductAttributeTable.as_view(), name='product_attribute_table'),
    url(r'^store_attribute_table/(?P<pk>\d+)$', views.StoreAttributeTable.as_view(), name='store_attribute_table'),
    url(r'^product_image_gallery/(?P<pk>\d+)$', views.ProductImageGallery.as_view(), name='product_image_gallery'),

    # Search multiple
    url(r'^search_result_product/(?P<keyword>.+)/$', views.SearchResultProduct.as_view(), name='search_result_product'),
    url(r'^search_result_store/(?P<keyword>.+)/$', views.SearchResultStore.as_view(), name='search_result_store'),

    # handsontable
    url(r'^handsontable/(?P<item>[\w]+)/$', views.MasterTableAPI.as_view(), name='handsontable'), # For DRF page
    url(r'^handsontable_header/(?P<item>[\w]+)/$', views.MasterTableHeaderAPI.as_view(), name='handsontable_header'), # For DRF page

    # RPC
    url(r'^procedure_run/(?P<item>[\w]+)/$', views.StoredProcedureAPI.as_view(), name='procedure_run'), # For DRF page
    url(r'^procedure_list$', views.StoredProcedureList.as_view(), name='procedure_list'),
    url(r'^download_screen$', views.DownloadScreen.as_view(), name='download_screen'),

    # Dashboard
    url(r'^store_map$', views.StoreMap.as_view(), name='store_map'),
    url(r'^store_map/(?P<pk>\d+)$', views.StoreMap.as_view(), name='store_map'),
    url(r'^store_map_api$', views.StoreMapAPI.as_view(), name='store_map_api'),
    url(r'^store_map_api/(?P<pk>\d+)$', views.StoreMapAPI.as_view(), name='store_map_api'),
    url(r'^historical_sales_table$', views.HistoricalSalesTable.as_view(), name='historical_sales_table'),
    url(r'^historical_sales_chart_api/$', views.HistoricalSalesChartAPI.as_view(), name='historical_sales_chart_api'),
    url(r'^historical_sales_chart_api/(?P<aggregation>[\w]+)/$', views.HistoricalSalesChartAPI.as_view(), name='historical_sales_chart_api'),
    url(r'^historical_sales_chart_api/(?P<aggregation>[\w]+)/(?P<category>[\w]+)/(?P<pk>\d+)$', views.HistoricalSalesChartAPI.as_view(), name='historical_sales_chart_api'),

    # wizard
    url(r'^iapcycle_update/(?P<dim_iapcycle_id>\d+)/(?P<is_completed>[01])$', views.IAPCycleUpdate.as_view(), name='iapcycle_update'),
    url(r'^iapfilter_update$', views.IAPFilterUserUpdate.as_view(), name='iapfilter_update'),

    # Store clustering
    url(r'^store_by_cluster_ai_api$', views.StoreByClusterAIAPI.as_view(), name='store_by_cluster_ai_api'),
    url(r'^store_by_cluster_user_api$', views.StoreByClusterUserAPI.as_view(), name='store_by_cluster_user_api'),
    url(r'^master_assortment_by_cluster$', views.FeatureProductInputByClusterTable.as_view(), name='master_assortment_by_cluster'),

    # Sales planning
    url(r'^sales_plan_by_month$', views.PlanByMonthTable.as_view(), name='sales_plan_by_month'),
    url(r'^consensus_sales_chart_api/(?P<aggregation>[\w]+)/$', views.ConsensusSalesChartAPI.as_view(), name='consensus_sales_chart_api'),
    url(r'^sales_plan_by_product_category$', views.PlanByProductCategoryTable.as_view(), name='sales_plan_by_product_category'),
    url(r'^sales_plan_by_product_category/(?P<level>[\w]+)$', views.PlanByProductCategoryTable.as_view(), name='sales_plan_by_product_category'),
    url(r'^sales_plan_by_product_category/(?P<level>[\w]+)/$', views.PlanByProductCategoryTable.as_view(), name='sales_plan_by_product_category'),
    url(r'^sales_plan_by_store$', views.PlanByStoreTable.as_view(), name='sales_plan_by_store'),
    url(r'^sales_plan_by_store(?P<level>[\w]+)$', views.PlanByStoreTable.as_view(), name='sales_plan_by_store'),
    url(r'^sales_plan_by_store/(?P<level>[\w]+)/$', views.PlanByStoreTable.as_view(), name='sales_plan_by_store'),
    url(r'^sales_plan_by_store/(?P<level>[\w]+)$', views.PlanByStoreTable.as_view(), name='sales_plan_by_store'),
    url(r'^sales_plan_by_store/(?P<level>[\w]+)/$', views.PlanByStoreTable.as_view(), name='sales_plan_by_store'),
    url(r'^sales_plan_chart_api/(?P<aggregation>[\w]+)/$', views.SalesPlanChartAPI.as_view(), name='sales_plan_chart_api'),
    url(r'^consolidated_plan_pivottable$', views.ConsolidatedPlanPivotTable.as_view(), name='consolidated_plan_pivottable'),

    # Range planning
    url(r'^range_architecture$', views.RangeArchitectureTable.as_view(), name='range_architecture'),
    url(r'^range_plan$', views.RangePlanTable.as_view(), name='range_plan'),
    url(r'^range_assortment$', views.RangeAssortmentTable.as_view(), name='range_assortment'),

    # Buy planning
    url(r'^buy_plan$', views.BuyPlanTable.as_view(), name='buy_plan'),


    # Strategic sales plan
    url(r'^strategic_sales_plan$', views.StrategicSalesPlanTable.as_view(), name='strategic_sales_plan'),
    url(r'^strategic_sales_plan/(?P<level>[\w]+)$', views.StrategicSalesPlanTable.as_view(), name='strategic_sales_plan'),
    url(r'^strategic_sales_plan/(?P<level>[\w]+)/$', views.StrategicSalesPlanTable.as_view(), name='strategic_sales_plan'),

    # Forecast
    url(r'^sales_forecast_api/$', views.SalesForecastAPI.as_view(), name='sales_forecast_api'),
    url(r'^sales_forecast_api/(?P<daterange_start>\d+-\d+-\d+)/(?P<daterange_end>\d+-\d+-\d+)/$', views.SalesForecastAPI.as_view(), name='sales_forecast_api'),
    # url(r'^sales_forecast_api/(?P<aggregation>[\w]+)/$', views.SalesForecastAPI.as_view(), name='sales_forecast_api'),
    # url(r'^sales_forecast_api/(?P<aggregation>[\w]+)/(?P<daterange_start>\d+-\d+-\d+)/(?P<daterange_end>\d+-\d+-\d+)/$', views.SalesForecastAPI.as_view(), name='sales_forecast_api'),
    # url(r'^sales_forecast_api/(?P<aggregation>[\w]+)/(?P<category>[\w]+)/(?P<pk>\d+)$', views.SalesForecastAPI.as_view(), name='sales_forecast_api'),

    # tokenfield
    url(r'^tokenfield_dimproduct_style$', views.TokenFieldDimProductStyle.as_view(), name='tokenfield_dimproduct_style'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
