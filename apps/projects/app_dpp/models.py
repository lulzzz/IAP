from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator

from core import mixins_model


class DimDemandCategory(models.Model):
    name = models.CharField(unique=True, max_length=45)

    def __str__(self):
        return self.name


class DimConstructionType(models.Model, mixins_model.ModelFormFieldNames):
    name = models.CharField(unique=True, max_length=45, verbose_name='construction type', validators=[RegexValidator(regex='^.{2,}$', message='Length must be at least 2', code='nomatch')])

    form_field_list = [
        'id',
        'name',
    ]

    class Meta:
        verbose_name = 'Construction Type'

    def __str__(self):
        return self.name


class DimLocation(models.Model, mixins_model.ModelFormFieldNames):
    region = models.CharField(max_length=45)
    country = models.CharField(unique=True, max_length=100)
    country_code_a2 = models.CharField(verbose_name='country code A2', unique=True, max_length=2, validators=[RegexValidator(regex='^.{2}$', message='Length must be 2', code='nomatch')])
    country_code_a3 = models.CharField(verbose_name='country code A3', unique=True, max_length=3, validators=[RegexValidator(regex='^.{3}$', message='Length must be 3', code='nomatch')])

    form_field_list = [
        'id',
        'region',
        'country',
        'country_code_a2',
        'country_code_a3'
    ]

    class Meta:
        verbose_name = 'Location'

    def __str__(self):
        return self.country


class DimDate(models.Model):
    id = models.IntegerField(primary_key=True)
    full_date = models.DateField()
    year = models.SmallIntegerField()
    year_cw = models.CharField(max_length=8)
    year_month = models.CharField(max_length=7)
    month_name = models.CharField(max_length=45)
    month_name_short = models.CharField(max_length=3)
    day_of_week = models.IntegerField()
    day_name_of_week = models.CharField(max_length=10)
    is_last_day_of_month = models.IntegerField()
    is_weekend_day = models.IntegerField()


class DimScenario(models.Model, mixins_model.ModelFormFieldNames):
    name = models.CharField(unique=True, max_length=45)
    tree_dict = models.TextField(blank=True, null=True)
    is_final = models.BooleanField(default=False)

    form_field_list = [
        'id',
        'name',
    ]

    class Meta:
        verbose_name = 'Scenario'


class DimRelease(models.Model):
    name = models.CharField(unique=True, max_length=45)
    dim_date = models.ForeignKey(DimDate, models.DO_NOTHING)
    comment = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class DimCustomer(models.Model, mixins_model.ModelFormFieldNames):
    dim_location = models.ForeignKey('DimLocation', models.DO_NOTHING, verbose_name='country code A2')
    # dim_location = models.ForeignKey('DimLocation', on_delete=models.CASCADE, verbose_name='country code A2')
    name = models.CharField(unique=True, max_length=100)
    market = models.CharField(max_length=45, blank=True, null=True)
    dc_plt = models.CharField(verbose_name='DC plant', max_length=45, blank=True, null=True)
    sold_to_party = models.CharField(max_length=45)
    sold_to_category = models.CharField(max_length=45, blank=True, null=True)
    is_active = models.BooleanField()
    is_placeholder = models.BooleanField()
    placeholder_level = models.CharField(max_length=45, blank=True, null=True)

    form_field_list = [
        'id',
        'dim_location',
        'name',
        'market',
        'dc_plt',
        'sold_to_party',
        'sold_to_category',
        'is_active',
        'is_placeholder',
        'placeholder_level',
    ]

    class Meta:
        verbose_name = 'Customer'


class DimFactory(models.Model, mixins_model.ModelFormFieldNames):
    dim_location = models.ForeignKey('DimLocation', models.DO_NOTHING, verbose_name='country code A2')
    plant_code = models.CharField(unique=True, max_length=45)
    vendor_code = models.CharField(max_length=45)
    vendor_name = models.CharField(max_length=200, blank=True, null=True)
    port = models.CharField(max_length=45, blank=True, null=True)
    is_active = models.BooleanField()
    is_placeholder = models.BooleanField(default=False)
    placeholder_level = models.CharField(max_length=45, blank=True, null=True)

    form_field_list = [
        'id',
        'plant_code',
        'vendor_code',
        'vendor_name',
        'port',
        'dim_location',
        'is_active',
    ]

    class Meta:
        verbose_name = 'Factory'

    def __str__(self):
        return self.short_name

    def get_absolute_url(self):
        return reverse(
            'search_tab_one_vendor',
            kwargs={'pk': self.pk}
        )

    @property
    def url(self):
        return self.get_absolute_url().replace('/', '#', 1)

    @property
    def link(self):
        return {
            'menu_item': 'search',
            'name': 'search_tab_one_vendor' + str(self.pk),
            'link': self.get_absolute_url().replace('/', '#', 1),
        }


class DimProductionLine(models.Model, mixins_model.ModelFormFieldNames):
    dim_factory = models.ForeignKey(DimFactory, models.DO_NOTHING, verbose_name='plant code')
    line = models.CharField(max_length=100)

    form_field_list = [
        'id',
        'dim_factory',
        'line',
    ]

    class Meta:
        verbose_name = 'Production Line'
        unique_together = (('dim_factory', 'line'),)



class HelperFactoryCapacityAdjustment(models.Model, mixins_model.ModelFormFieldNames):
    plant_code = models.CharField(unique=True, max_length=45)
    percentage = models.FloatField()
    percentage_adjustment = models.FloatField()

    form_field_list = [
        'id',
        'plant_code',
        'percentage',
        'percentage_adjustment',
    ]

    class Meta:
        verbose_name = 'Factory Capacity Adjustment'



class HelperMapping(models.Model, mixins_model.ModelFormFieldNames):
    category = models.CharField(max_length=100)
    parent = models.CharField(max_length=200)
    child = models.CharField(max_length=100)
    comment = models.CharField(max_length=1000, blank=True, null=True)

    form_field_list = [
        'id',
        'category',
        'parent',
        'child',
    ]

    class Meta:
        unique_together = (('category', 'child'),)
        verbose_name = 'Mapping'


class SourceMetadata(models.Model, mixins_model.ModelFormFieldNames):
    table_name = models.CharField(max_length=100)
    etl_type = models.CharField(max_length=45)
    src_name = models.CharField(verbose_name='source file', max_length=100)
    timestamp_file = models.DateTimeField(verbose_name='last modified date')
    state = models.CharField(max_length=3)

    form_field_list = [
        'src_name',
        'timestamp_file',
    ]


class SystemLogFile(models.Model, mixins_model.ModelFormFieldNames):
    system = models.CharField(max_length=30)
    source = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    value = models.CharField(max_length=300)

    form_field_list = [
        'source',
        'category',
        'value',
    ]


class DimProduct(models.Model, mixins_model.ModelFormFieldNames):
    dim_construction_type = models.ForeignKey(DimConstructionType, models.DO_NOTHING)
    material = models.CharField(unique=True, max_length=45)
    material_text_short = models.CharField(max_length=200, blank=True, null=True)
    material_description = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=200, blank=True, null=True)
    main_description = models.CharField(max_length=200, blank=True, null=True)
    group_description = models.CharField(max_length=200, blank=True, null=True)
    family = models.CharField(max_length=200, blank=True, null=True)
    pgs = models.CharField(verbose_name='PGS', max_length=200, blank=True, null=True)
    segment_description = models.CharField(max_length=200, blank=True, null=True)
    gender_label = models.CharField(max_length=200, blank=True, null=True)
    product_type = models.CharField(max_length=200, blank=True, null=True)
    business_life_cyle = models.IntegerField(default=0)
    is_placeholder = models.BooleanField(default=False)
    placeholder_level = models.CharField(max_length=45, blank=True, null=True)

    form_field_list = [
        'id',
        'material',
        'material_text_short',
        'material_description',
        'status',
        'main_description',
        'group_description',
        'family',
        'pgs',
        'segment_description',
        'gender_label',
        'product_type',
        'business_life_cyle',
    ]

    class Meta:
        verbose_name = 'Product'

    def __str__(self):
        return self.sku

    def get_absolute_url(self):
        return reverse(
            'search_tab_one_product',
            kwargs={'pk': self.pk}
        )

    @property
    def url(self):
        return self.get_absolute_url().replace('/', '#', 1)

    @property
    def link(self):
        return {
            'menu_item': 'search',
            'name': 'search_tab_one_product' + str(self.pk),
            'link': self.get_absolute_url().replace('/', '#', 1),
        }


class FactDemand(models.Model, mixins_model.ModelFormFieldNames):
    dim_release = models.ForeignKey(DimRelease, models.DO_NOTHING)
    dim_demand_category = models.ForeignKey(DimDemandCategory, models.DO_NOTHING)
    # dim_customer = models.ForeignKey(DimCustomer, models.DO_NOTHING)
    dim_product = models.ForeignKey(DimProduct, models.DO_NOTHING)
    dim_date_month_xf = models.ForeignKey(DimDate, models.DO_NOTHING)
    quantity = models.IntegerField(default= 0)

    form_field_list = []


class FactDemandAllocation(models.Model):
    dim_release = models.ForeignKey(DimRelease, models.DO_NOTHING)
    dim_scenario = models.ForeignKey(DimScenario, models.DO_NOTHING)
    dim_demand_category = models.ForeignKey(DimDemandCategory, models.DO_NOTHING)
    # dim_customer = models.ForeignKey(DimCustomer, models.DO_NOTHING)
    dim_product = models.ForeignKey(DimProduct, models.DO_NOTHING)

    dim_production_line = models.ForeignKey(DimProductionLine, models.DO_NOTHING)
    dim_date_month_xf = models.ForeignKey(DimDate, models.DO_NOTHING)
    quantity = models.IntegerField(default= 0)
    allocation_logic = models.CharField(max_length=1000, blank=True, null=True)

    dim_production_line_user = models.ForeignKey(DimProductionLine, models.DO_NOTHING, related_name='dim_production_line_user')
    dim_date_month_xf_user = models.ForeignKey(DimDate, models.DO_NOTHING, related_name='dim_date_month_xf_user')
    quantity_user = models.IntegerField(default=0)
    comment_user = models.CharField(max_length=1000, blank=True, null=True)


class FactCapacity(models.Model, mixins_model.ModelFormFieldNames):
    dim_release = models.ForeignKey(DimRelease, models.DO_NOTHING, default=1)
    dim_production_line = models.ForeignKey(DimProductionLine, models.DO_NOTHING, verbose_name='production line')
    # dim_customer = models.ForeignKey(DimCustomer, models.DO_NOTHING)
    # dim_construction_type = models.ForeignKey(DimConstructionType, models.DO_NOTHING)
    dim_date_month_xf = models.ForeignKey(DimDate, models.DO_NOTHING, verbose_name='month')
    quantity = models.IntegerField(default= 0)

    form_field_list = [
        'id',
        'dim_production_line',
        'dim_date',
        'quantity',
    ]

    class Meta:
        unique_together = (('dim_release', 'dim_production_line', 'dim_date_month_xf'),)
        verbose_name = 'Capacity'


class HelperReleaseCurrent(models.Model):
    dim_release = models.ForeignKey(DimRelease, models.DO_NOTHING, verbose_name='release')

    class Meta:
        verbose_name = 'Current Release'



class HelperScenario01(models.Model):

    decision01 = models.CharField(max_length=3, choices=CATEGORIES, verbose_name='capacity priority')

    CATEGORIES = (
        ('COM', 'Combat'),
        ('CRA', 'Crafting'),
        ('WAR', 'Warfare'),
    )

    class Meta:
        verbose_name = 'Current Release'
