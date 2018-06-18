from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator

from core import mixins_model


class DimDemandCategory(models.Model):
    name = models.CharField(unique=True, max_length=45)

    class Meta:
        db_table = 'dim_demand_category'

    def __str__(self):
        return self.name


class DimBusiness(models.Model, mixins_model.ModelFormFieldNames):
    brand = models.CharField(max_length=45)
    product_line = models.CharField(max_length=45)

    class Meta:
        db_table = 'dim_business'
        unique_together = (('brand', 'product_line'),)

    def __str__(self):
        return self.brand + ' - ' + self.product_line


class DimBuyingProgram(models.Model):
    category = models.CharField(max_length=45, blank=True, null=True)
    name = models.CharField(max_length=45)
    name_short = models.CharField(max_length=45, blank=True, null=True)
    dim_business = models.ForeignKey(DimBusiness, models.DO_NOTHING)

    class Meta:
        db_table = 'dim_buying_program'
        unique_together = (('id', 'dim_business'),)

    def __str__(self):
        return self.name


class DimConstructionType(models.Model, mixins_model.ModelFormFieldNames):
    name = models.CharField(unique=True, max_length=45, verbose_name='construction type', validators=[RegexValidator(regex='^.{2,}$', message='Length must be at least 2', code='nomatch')])

    form_field_list = [
        'id',
        'name',
    ]

    class Meta:
        db_table = 'dim_construction_type'
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
        db_table = 'dim_location'
        verbose_name = 'Location'

    def __str__(self):
        return self.country


class DimDate(models.Model):
    id = models.IntegerField(primary_key=True)
    full_date = models.DateField()
    season_buy = models.CharField(max_length=45)
    season_year_buy = models.CharField(max_length=45)
    season_year_short_buy = models.CharField(max_length=4)
    season_crd = models.CharField(max_length=45, blank=True, null=True)
    season_year_crd = models.CharField(max_length=45, blank=True, null=True)
    season_year_short_crd = models.CharField(max_length=4, blank=True, null=True)
    season_intro = models.CharField(max_length=45, blank=True, null=True)
    season_year_intro = models.CharField(max_length=45, blank=True, null=True)
    season_year_short_intro = models.CharField(max_length=4, blank=True, null=True)
    year_accounting = models.SmallIntegerField()
    year_cw_accounting = models.CharField(max_length=8)
    year_month_accounting = models.CharField(max_length=7)
    month_name_accounting = models.CharField(max_length=45)
    month_name_short_accounting = models.CharField(max_length=3)
    day_of_week = models.IntegerField()
    day_name_of_week = models.CharField(max_length=10)
    is_last_day_of_month = models.IntegerField()
    is_weekend_day = models.IntegerField()

    class Meta:
        db_table = 'dim_date'


class DimRelease(models.Model, mixins_model.ModelFormFieldNames):
    dim_demand_category = models.ForeignKey(DimDemandCategory, models.DO_NOTHING, verbose_name='demand category')
    dim_buying_program = models.ForeignKey(DimBuyingProgram, models.DO_NOTHING, verbose_name='buying program')
    buy_month = models.CharField(max_length=45)
    dim_date = models.ForeignKey(DimDate, models.DO_NOTHING, verbose_name='date')
    comment = models.CharField(max_length=100)

    form_field_list = [
        'id',
        'dim_demand_category',
        'dim_buying_program',
        'buy_month',
        'dim_date',
        'comment',
    ]

    class Meta:
        db_table = 'dim_release'
        unique_together = (('dim_demand_category', 'dim_buying_program', 'buy_month', 'comment'),)
        verbose_name = 'Release'

    def __str__(self):
        return self.comment


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
        db_table = 'dim_customer'
        verbose_name = 'Customer'


class DimFactory(models.Model, mixins_model.ModelFormFieldNames):
    dim_location = models.ForeignKey('DimLocation', models.DO_NOTHING, verbose_name='country code A2')
    dim_business = models.ForeignKey(DimBusiness, models.DO_NOTHING, default=1)
    vendor_group = models.CharField(max_length=45)
    short_name = models.CharField(unique=True, max_length=45)
    long_name = models.CharField(max_length=200, blank=True, null=True)
    port = models.CharField(max_length=45, blank=True, null=True)
    allocation_group = models.CharField(max_length=45)
    valid_acadia_fty_plant_code = models.CharField(max_length=45, blank=True, null=True)
    valid_acadia_vendor_code_1505_1510 = models.CharField(max_length=45, blank=True, null=True)
    valid_acadia_vendor_code_1550_mexico = models.CharField(max_length=45, blank=True, null=True)
    condor_factory_code_brazil = models.CharField(max_length=45, blank=True, null=True)
    condor_vendor_code_brazil = models.CharField(max_length=45, blank=True, null=True)
    condor_factory_code_chile = models.CharField(max_length=45, blank=True, null=True)
    condor_vendor_code_chile = models.CharField(max_length=45, blank=True, null=True)
    eu_supplier_code = models.CharField(max_length=45, blank=True, null=True)
    reva_vendor_fty = models.CharField(max_length=45, blank=True, null=True)
    reva_agent_vendor = models.CharField(max_length=45, blank=True, null=True)
    is_active = models.BooleanField()
    is_placeholder = models.BooleanField()
    placeholder_level = models.CharField(max_length=45, blank=True, null=True)

    form_field_list = [
        'id',
        'dim_location',
        'vendor_group',
        'short_name',
        'long_name',
        'port',
        'allocation_group',
        'valid_acadia_fty_plant_code',
        'valid_acadia_vendor_code_1505_1510',
        'valid_acadia_vendor_code_1550_mexico',
        'condor_factory_code_brazil',
        'condor_vendor_code_brazil',
        'condor_factory_code_chile',
        'condor_vendor_code_chile',
        'eu_supplier_code',
        'reva_vendor_fty',
        'reva_agent_vendor',
        'is_active',
        'is_placeholder',
        'placeholder_level',
    ]

    class Meta:
        db_table = 'dim_factory'
        unique_together = (('id', 'dim_business'),)
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


class HelperPdasFootwearVansAvgFob(models.Model, mixins_model.ModelFormFieldNames):
    factory_short_name = models.CharField(verbose_name='factory code', max_length=45)
    material_id = models.CharField(verbose_name='MTL#', max_length=45)
    fob = models.FloatField(verbose_name='FOB',)

    form_field_list = [
        'id',
        'factory_short_name',
        'material_id',
        'fob',
    ]

    class Meta:
        db_table = 'helper_pdas_footwear_vans_avg_fob'
        unique_together = (('factory_short_name', 'material_id'),)
        verbose_name = 'FOB Confirmation'


class HelperPdasFootwearVansCutoff(models.Model, mixins_model.ModelFormFieldNames):
    country_code_a2 = models.CharField(verbose_name='country code A2', max_length=2)
    port_code = models.CharField(verbose_name='port code', max_length=45)
    port_name = models.CharField(verbose_name='port name', max_length=45)
    cutoff_day_eu_dc = models.CharField(verbose_name='cutoff day EU DC', max_length=45)
    cutoff_day_eu_crossdock = models.CharField(verbose_name='cutoff day EU Crossdock', max_length=45)
    comment = models.CharField(max_length=1000, blank=True, null=True)

    form_field_list = [
        'id',
        'country_code_a2',
        'port_code',
        'port_name',
        'cutoff_day_eu_dc',
        'cutoff_day_eu_crossdock',
        'comment',
    ]

    class Meta:
        db_table = 'helper_pdas_footwear_vans_cutoff'
        unique_together = (('country_code_a2', 'port_code'),)
        verbose_name = 'Cutoff EMEA'


class HelperPdasFootwearVansFactoryCapacityAdjustment(models.Model, mixins_model.ModelFormFieldNames):
    factory_short_name = models.CharField(verbose_name='factory code', unique=True, max_length=45)
    percentage = models.FloatField()
    percentage_adjustment = models.FloatField()

    form_field_list = [
        'id',
        'factory_short_name',
        'percentage',
        'percentage_adjustment',
    ]

    class Meta:
        db_table = 'helper_pdas_footwear_vans_factory_capacity_adjustment'
        verbose_name = 'Factory Capacity Adjustment'


class HelperPdasFootwearVansFactoryCapacityByRegion(models.Model, mixins_model.ModelFormFieldNames):
    factory_short_name = models.CharField(verbose_name='factory code', unique=True, max_length=45)
    emea = models.FloatField(verbose_name='EMEA')
    apac = models.FloatField(verbose_name='APAC')
    casa = models.FloatField(verbose_name='CASA')
    nora = models.FloatField(verbose_name='NORA')

    form_field_list = [
        'id',
        'factory_short_name',
        'emea',
        'apac',
        'casa',
        'nora',
    ]

    class Meta:
        db_table = 'helper_pdas_footwear_vans_factory_capacity_by_region'
        verbose_name = 'Factory Capacity by Region'


class HelperPdasFootwearVansFtyQt(models.Model, mixins_model.ModelFormFieldNames):
    material_id = models.CharField(verbose_name='MTL#', max_length=45)
    factory_short_name = models.CharField(max_length=45)
    qt_leadtime = models.IntegerField(verbose_name='QT leadtime')
    comment = models.CharField(max_length=1000, blank=True, null=True)

    form_field_list = [
        'id',
        'material_id',
        'factory_short_name',
        'qt_leadtime',
        'comment',
    ]

    class Meta:
        db_table = 'helper_pdas_footwear_vans_fty_qt'
        unique_together = (('material_id', 'factory_short_name'),)
        verbose_name = 'Factory QT'


class HelperPdasFootwearVansLabelUpcharge(models.Model, mixins_model.ModelFormFieldNames):
    customer_name = models.CharField(max_length=45)
    product_type = models.CharField(max_length=45)
    label_upcharge = models.FloatField()

    form_field_list = [
        'id',
        'customer_name',
        'product_type',
        'label_upcharge',
    ]

    class Meta:
        db_table = 'helper_pdas_footwear_vans_label_upcharge'
        unique_together = (('customer_name', 'product_type'),)
        verbose_name = 'Label Upcharge'


class HelperPdasFootwearVansMapping(models.Model, mixins_model.ModelFormFieldNames):
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
        db_table = 'helper_pdas_footwear_vans_mapping'
        unique_together = (('category', 'child'),)
        verbose_name = 'Mapping'


class HelperPdasFootwearVansMoqPolicy(models.Model, mixins_model.ModelFormFieldNames):
    product_type = models.CharField(max_length=45)
    from_by_region = models.IntegerField()
    to_by_region = models.IntegerField()
    from_by_customer = models.IntegerField()
    to_by_customer = models.IntegerField()
    upcharge = models.FloatField(default=0)
    reject = models.CharField(default='No', max_length=3)
    comment = models.CharField(max_length=1000, blank=True, null=True)

    form_field_list = [
        'id',
        'product_type',
        'from_by_region',
        'to_by_region',
        'from_by_customer',
        'to_by_customer',
        'upcharge',
        'reject',
        'comment',
    ]

    class Meta:
        db_table = 'helper_pdas_footwear_vans_moq_policy'
        verbose_name = 'MOQ Policy'


class HelperPdasFootwearVansPrebuild(models.Model, mixins_model.ModelFormFieldNames):
    region = models.CharField(max_length=45)
    material_id = models.CharField(verbose_name='MTL#', max_length=45)
    size = models.CharField(max_length=45)
    factory_short_name = models.CharField(verbose_name='factory code', max_length=45)
    current_balance = models.IntegerField()
    buying_program_name = models.CharField(max_length=45)
    status = models.CharField(max_length=45)
    cancellation_cost_per_unit = models.FloatField()
    comment = models.CharField(max_length=1000, blank=True, null=True)

    form_field_list = [
        'id',
        'region',
        'material_id',
        'size',
        'factory_short_name',
        'current_balance',
        'buying_program_name',
        'status',
        'cancellation_cost_per_unit',
        'comment',
    ]

    class Meta:
        db_table = 'helper_pdas_footwear_vans_prebuild'
        unique_together = (('region', 'material_id', 'size', 'factory_short_name', 'buying_program_name'),)
        verbose_name = 'Prebuild Balance'


class HelperPdasFootwearVansRetailQt(models.Model, mixins_model.ModelFormFieldNames):
    status = models.CharField(max_length=45)
    region = models.CharField(max_length=45)
    sold_to_party = models.CharField(max_length=45)
    material_id = models.CharField(verbose_name='MTL#', max_length=45)
    factory_short_name = models.CharField(verbose_name='factory code', max_length=45)
    buying_program_name = models.CharField(max_length=45)
    comment = models.CharField(max_length=1000, blank=True, null=True)

    form_field_list = [
        'id',
        'status',
        'region',
        'sold_to_party',
        'material_id',
        'factory_short_name',
        'buying_program_name',
        'comment',
    ]

    class Meta:
        db_table = 'helper_pdas_footwear_vans_retail_qt'
        unique_together = (('region', 'sold_to_party', 'material_id', 'factory_short_name'),)
        verbose_name = 'Retail QT'


class PdasMetadata(models.Model, mixins_model.ModelFormFieldNames):
    table_name = models.CharField(max_length=100)
    etl_type = models.CharField(max_length=45)
    src_name = models.CharField(verbose_name='source file', max_length=100)
    timestamp_file = models.DateTimeField(verbose_name='last modified date')
    state = models.CharField(max_length=3)

    form_field_list = [
        'src_name',
        'timestamp_file',
    ]

    class Meta:
        db_table = 'pdas_metadata'


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

    class Meta:
        db_table = 'system_log_file'


class HelperPdasFootwearVansReleaseCurrent(models.Model):
    dim_release = models.ForeignKey(DimRelease, models.DO_NOTHING, verbose_name='release')

    class Meta:
        db_table = 'helper_pdas_footwear_vans_release_current'
        verbose_name = 'Current Release'


class HelperPdasFootwearVansPerformance(models.Model, mixins_model.ModelFormFieldNames):
    days_delay = models.IntegerField(verbose_name='days of delay')
    delivery_performance = models.CharField(max_length=45)

    form_field_list = [
        'id',
        'days_delay',
        'delivery_performance',
    ]

    class Meta:
        db_table = 'helper_pdas_footwear_vans_performance'
        verbose_name = 'Performance'


class DimProduct(models.Model, mixins_model.ModelFormFieldNames):
    dim_business = models.ForeignKey(DimBusiness, models.DO_NOTHING)
    material_id = models.CharField(verbose_name='MTL #', max_length=45)
    size = models.CharField(max_length=45)
    style_id = models.CharField(verbose_name='style #', max_length=45)
    style_id_erp = models.CharField(max_length=45, blank=True, null=True)
    material_description = models.CharField(max_length=100, blank=True, null=True)
    material_description_erp = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=45, blank=True, null=True)
    style_name = models.CharField(max_length=100, blank=True, null=True)
    style_name_new = models.CharField(max_length=45, blank=True, null=True)
    color_description = models.CharField(max_length=100)
    color_description_erp = models.CharField(max_length=100, blank=True, null=True)
    product_type = models.CharField(max_length=45, blank=True, null=True)
    cat_sub_sbu = models.CharField(max_length=45, blank=True, null=True)
    gender = models.CharField(max_length=45, blank=True, null=True)
    gender_new = models.CharField(max_length=45, blank=True, null=True)
    lifecycle = models.CharField(max_length=45)
    product_cycle = models.CharField(max_length=45, blank=True, null=True)
    style_complexity = models.CharField(max_length=45)
    dim_construction_type = models.ForeignKey(DimConstructionType, models.DO_NOTHING)
    production_lt = models.IntegerField(verbose_name='production LT', blank=True, null=True)
    pre_build_mtl = models.NullBooleanField(verbose_name='prebuild MTL', blank=True, null=True)
    qt_mtl = models.NullBooleanField(verbose_name='QT MTL', blank=True, null=True)
    clk_mtl = models.NullBooleanField(verbose_name='CLK MTL', blank=True, null=True)
    sjd_mtl = models.NullBooleanField(verbose_name='SJD MTL', blank=True, null=True)
    dtp_mtl = models.NullBooleanField(verbose_name='DTP MTL', blank=True, null=True)
    brt_in_house = models.NullBooleanField(verbose_name='BRT MTL', blank=True, null=True)
    material_id_emea = models.CharField(verbose_name='MAT # EMEA', max_length=45, blank=True, null=True)
    sku = models.CharField(verbose_name='SKU', max_length=45, blank=True, null=True)
    # is_hypercare = models.NullBooleanField(blank=True, null=True)
    is_placeholder = models.BooleanField()
    placeholder_level = models.CharField(max_length=45, blank=True, null=True)

    form_field_list = []

    class Meta:
        db_table = 'dim_product'
        unique_together = (('material_id', 'size'),)

    def __str__(self):
        return self.material_id + ' ' + self.size

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


class FactDemandTotal(models.Model, mixins_model.ModelFormFieldNames):
    dim_release = models.ForeignKey(DimRelease, models.DO_NOTHING)
    dim_business = models.ForeignKey(DimBusiness, models.DO_NOTHING)
    dim_buying_program = models.ForeignKey(DimBuyingProgram, models.DO_NOTHING)
    dim_product = models.ForeignKey(DimProduct, models.DO_NOTHING)
    dim_date = models.ForeignKey(DimDate, models.DO_NOTHING)
    dim_date_id_buy_month = models.ForeignKey(DimDate, models.DO_NOTHING, db_column='dim_date_id_buy_month', related_name='dim_date_id_buy_month')
    dim_date_forecast_vs_actual = models.IntegerField(blank=True, null=True)
    dim_factory_id_original_unconstrained = models.ForeignKey(DimFactory, models.DO_NOTHING, db_column='dim_factory_id_original_unconstrained', related_name='dim_factory_id_original_unconstrained')
    dim_factory_id_original_constrained = models.ForeignKey(DimFactory, models.DO_NOTHING, db_column='dim_factory_id_original_constrained', related_name='dim_factory_id_original_constrained')
    dim_factory = models.ForeignKey(DimFactory, models.DO_NOTHING, related_name='dim_factory_id')
    dim_factory_id_final = models.ForeignKey(DimFactory, models.DO_NOTHING, db_column='dim_factory_id_final', related_name='dim_factory_id_final')
    dim_customer = models.ForeignKey(DimCustomer, models.DO_NOTHING)
    dim_demand_category = models.ForeignKey(DimDemandCategory, models.DO_NOTHING)
    order_status = models.CharField(max_length=45, blank=True, null=True)
    order_number = models.CharField(max_length=45)
    pr_code = models.CharField(max_length=45, blank=True, null=True)
    pr_cut_code = models.CharField(max_length=45, blank=True, null=True)
    po_code_customer = models.CharField(max_length=45, blank=True, null=True)
    so_code = models.CharField(max_length=45, blank=True, null=True)
    is_asap = models.IntegerField()
    quantity_lum = models.IntegerField(blank=True, null=True)
    quantity_non_lum = models.IntegerField(blank=True, null=True)
    quantity_region_mtl_lvl = models.IntegerField(blank=True, null=True)
    quantity_customer_mtl_lvl = models.IntegerField(blank=True, null=True)
    comment_vfa = models.CharField(max_length=1000, blank=True, null=True)
    edit_dt = models.DateTimeField(blank=True, null=True)
    allocation_logic_unconstrained = models.CharField(max_length=1000, blank=True, null=True)
    allocation_logic_constrained = models.CharField(max_length=1000, blank=True, null=True)
    customer_moq = models.IntegerField(blank=True, null=True)
    customer_below_moq = models.IntegerField(blank=True, null=True)
    region_moq = models.IntegerField(blank=True, null=True)
    region_below_moq = models.IntegerField(blank=True, null=True)
    upcharge = models.FloatField(blank=True, null=True)
    is_rejected = models.IntegerField(blank=True, null=True)
    material_sr = models.CharField(max_length=45, blank=True, null=True)
    component_factory_short_name = models.CharField(max_length=45, blank=True, null=True)
    production_lt_actual_buy = models.IntegerField(blank=True, null=True)
    production_lt_actual_vendor = models.IntegerField(blank=True, null=True)
    comment_region = models.CharField(max_length=1000, blank=True, null=True)
    sold_to_customer_name = models.CharField(max_length=100, blank=True, null=True)
    mcq = models.IntegerField(blank=True, null=True)
    musical_cnt = models.CharField(max_length=45, blank=True, null=True)
    delivery_d = models.DateField(blank=True, null=True)
    confirmed_price_in_solid_size = models.FloatField(blank=True, null=True)
    fabriq_moq = models.IntegerField(blank=True, null=True)
    confirmed_crd_dt = models.DateField(blank=True, null=True)
    confirmed_unit_price_memo = models.CharField(max_length=45, blank=True, null=True)
    confirmed_unit_price_po = models.FloatField(blank=True, null=True)
    cy_csf_load = models.CharField(max_length=45, blank=True, null=True)
    min_surcharge = models.CharField(max_length=45, blank=True, null=True)
    confirmed_unit_price_vendor = models.CharField(max_length=45, blank=True, null=True)
    nominated_supplier_name = models.CharField(max_length=45, blank=True, null=True)
    comment_vendor = models.CharField(max_length=45, blank=True, null=True)
    confirmed_comp_eta_hk = models.CharField(max_length=45, blank=True, null=True)
    comment_comp_factory = models.CharField(max_length=45, blank=True, null=True)
    buy_comment = models.CharField(max_length=1000, blank=True, null=True)
    status_orig_req = models.IntegerField(blank=True, null=True)
    performance_orig_req = models.CharField(max_length=45, blank=True, null=True)
    smu = models.CharField(max_length=45, blank=True, null=True)
    order_reference = models.CharField(max_length=45, blank=True, null=True)
    sku_footlocker = models.CharField(max_length=45, blank=True, null=True)
    prepack_code = models.CharField(max_length=45, blank=True, null=True)
    exp_delivery_with_constraint = models.CharField(max_length=45, blank=True, null=True)
    exp_delivery_without_constraint = models.CharField(max_length=45, blank=True, null=True)
    coo = models.CharField(max_length=45, blank=True, null=True)
    remarks_region = models.CharField(max_length=100, blank=True, null=True)
    need_to_reallocate = models.CharField(max_length=45, blank=True, null=True)

    form_field_list = []

    class Meta:
        db_table = 'fact_demand_total'


class FactFactoryCapacity(models.Model):
    dim_business = models.ForeignKey(DimBusiness, models.DO_NOTHING)
    dim_factory = models.ForeignKey(DimFactory, models.DO_NOTHING)
    dim_customer = models.ForeignKey(DimCustomer, models.DO_NOTHING)
    dim_construction_type = models.ForeignKey(DimConstructionType, models.DO_NOTHING)
    dim_date = models.ForeignKey(DimDate, models.DO_NOTHING)
    capacity_raw_daily = models.IntegerField()
    capacity_raw_weekly = models.IntegerField()
    capacity_raw_daily_overwritten = models.IntegerField()
    capacity_raw_weekly_overwritten = models.IntegerField()
    capacity_available_weekly = models.IntegerField()
    capacity_available_weekly_adjusted = models.IntegerField()
    percentage_region = models.FloatField()
    percentage_from_original = models.FloatField()

    class Meta:
        db_table = 'fact_factory_capacity'
        unique_together = (('dim_business', 'dim_factory', 'dim_customer', 'dim_construction_type', 'dim_date'),)


class FactPriorityList(models.Model):
    dim_release = models.ForeignKey(DimRelease, models.DO_NOTHING)
    dim_business = models.ForeignKey(DimBusiness, models.DO_NOTHING)
    dim_product = models.ForeignKey(DimProduct, models.DO_NOTHING)
    dim_factory_id_1 = models.ForeignKey(DimFactory, models.DO_NOTHING, db_column='dim_factory_id_1')
    dim_factory_id_2 = models.IntegerField(blank=True, null=True)
    production_lt = models.IntegerField(blank=True, null=True)
    llt = models.CharField(max_length=45, blank=True, null=True)
    co_cu_new = models.CharField(max_length=45, blank=True, null=True)
    asia_development_buy_ready = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'fact_priority_list'
        unique_together = (('dim_release', 'dim_business', 'dim_product'),)
