from . import models

class DMSFilter():

    def init_class_dict_mixin(self):

        # Check if user has done a selection
        user_filter_query = models.DimIAPFilterUser.objects.filter(user=self.user)
        if user_filter_query.exists():
            user_filter = user_filter_query.get()
            self.dim_channel_id = user_filter.dim_iapfilter.dim_channel_id
            self.sales_year = user_filter.dim_iapfilter.sales_year
            self.sales_season = user_filter.dim_iapfilter.sales_season
        else:
            self.dim_channel_id = 1
            self.sales_year = 2017
            self.sales_season = 'SS'
            user_filter_query = models.DimIAPFilterUser(
                user=self.user,
                dim_iapfilter=models.DimIAPFilter.objects.filter(
                    dim_channel_id=self.dim_channel_id,
                    sales_year=self.sales_year,
                    sales_season=self.sales_season,
                ).get(),
            )
            user_filter_query.save()

        # Set filter
        dim_iapfilter_queryset = models.DimIAPFilter.objects.filter(
            dim_channel_id=self.dim_channel_id,
            sales_year=self.sales_year,
            sales_season=self.sales_season,
        ).get()
        self.dim_iapfilter = dim_iapfilter_queryset.id
        self.dim_channel_name = dim_iapfilter_queryset.dim_channel.name
        self.dim_iapfilter_label = dim_iapfilter_queryset.get_label()
        self.consolidated_plan_file = 'Consolidated Plan - ' + self.dim_iapfilter_label + '.xlsx'

        self.filter_dict['dim_iapfilter'] = self.dim_iapfilter
