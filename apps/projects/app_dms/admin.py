from django.contrib import admin

from .models import DimIAPStep
from .models import DimIAPCycle


# DimIAPStep
class DimIAPStepAdmin(admin.ModelAdmin):

    list_display = ('name', 'position')
    # search_fields = ('name', 'code')

admin.site.register(DimIAPStep, DimIAPStepAdmin)


# DimIAPCycle
class DimIAPCycleAdmin(admin.ModelAdmin):

    readonly_fields = ['dim_iapfilter', 'dim_iapstep']

    list_display = (
        'get_dim_iapfilter_sales_year',
        'get_dim_iapfilter_sales_season',
        'get_dim_iapfilter_channel_name',
        'get_dim_iapstep_name',
        'get_dim_iapstep_position',
        'is_completed',
        'completion_dt',
    )

    def get_dim_iapfilter_sales_year(self, obj):
        return obj.dim_iapfilter.sales_year
    get_dim_iapfilter_sales_year.short_description = 'Sales Year'
    get_dim_iapfilter_sales_year.admin_order_field = 'dim_iapfilter__sales_year'

    def get_dim_iapfilter_sales_season(self, obj):
        return obj.dim_iapfilter.sales_season
    get_dim_iapfilter_sales_season.short_description = 'Sales Season'
    get_dim_iapfilter_sales_season.admin_order_field = 'dim_iapfilter__sales_season'

    def get_dim_iapfilter_channel_name(self, obj):
        return obj.dim_iapfilter.dim_channel.name
    get_dim_iapfilter_channel_name.short_description = 'Channel'
    get_dim_iapfilter_channel_name.admin_order_field = 'dim_iapfilter__dim_channel__name'

    def get_dim_iapstep_name(self, obj):
        return obj.dim_iapstep.name
    get_dim_iapstep_name.short_description = 'Step Name'

    def get_dim_iapstep_position(self, obj):
        return obj.dim_iapstep.position
    get_dim_iapstep_position.short_description = 'Step Position'
    get_dim_iapstep_position.admin_order_field = 'dim_iapstep__position'

    list_filter = (
        ('is_completed', admin.AllValuesFieldListFilter),
    )

admin.site.register(DimIAPCycle, DimIAPCycleAdmin)
