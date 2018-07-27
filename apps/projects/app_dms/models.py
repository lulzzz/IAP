from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

from core import mixins_model

r"""
Retailisation master format
"""
class KPI(models.Model):
    salesdate = models.DateTimeField(blank=True, null=True)
    salescomp = models.IntegerField(blank=True, null=True)
    locationcode = models.IntegerField(blank=True, null=True)
    salesunits = models.IntegerField(blank=True, null=True)
    netretailsaleslocal = models.BigIntegerField(blank=True, null=True)
    netretailsaleseur = models.BigIntegerField(blank=True, null=True)
    currency = models.CharField(max_length=500, blank=True, null=True)
    transactions = models.IntegerField(blank=True, null=True)
    upt = models.IntegerField(blank=True, null=True)
    avtlocal = models.IntegerField(blank=True, null=True)
    avteur = models.IntegerField(blank=True, null=True)
    ppplocal = models.FloatField(blank=True, null=True)
    pppeur = models.FloatField(blank=True, null=True)



r"""
Converted master format
"""
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
    year_month_name = models.CharField(max_length=7) # e.g. 2017-01

    sales_season = models.CharField(max_length=2) # e.g. FW
    sales_year = models.IntegerField() # e.g. 2017
    sales_cw = models.CharField(max_length=100) # e.g. 52


class DimChannel(models.Model, mixins_model.ModelFormFieldNames):
    r'''
    Model for channel master
    '''
    name = models.CharField(max_length=100)

    form_field_list = [
        'id',
        'name',
    ]

    class Meta:
        verbose_name = 'Channel'

    def __str__(self):
        return self.name


class DimProduct(models.Model, mixins_model.ModelFormFieldNames):
    id = models.IntegerField(primary_key=True)
    productcode = models.CharField(verbose_name='product code', unique=True, max_length=100)
    productshortdescription = models.CharField(verbose_name='short description', max_length=100, blank=True, null=True)
    productdescription = models.CharField(verbose_name='description', max_length=100, blank=True, null=True)
    size = models.CharField(max_length=100, blank=True, null=True)
    colour = models.CharField(max_length=100, blank=True, null=True)
    style = models.CharField(max_length=500, blank=True, null=True)
    category = models.CharField(max_length=500, blank=True, null=True)
    division = models.CharField(max_length=500, blank=True, null=True)
    essential_trend = models.CharField(max_length=100, blank=True, null=True)
    basic_fashion = models.CharField(max_length=100, blank=True, null=True)
    quality = models.IntegerField(blank=True, null=True)
    image = models.CharField(max_length=500, blank=True, null=True)

    form_field_list = [
        'id',
        'productcode',
        'productdescription',
        'size',
        'style',
        'colour',
        'category',
        'division',
    ]

    def get_absolute_url(self):
        return reverse(
            'search_tab_one_product',
            kwargs={
                'pk': self.pk
            }
        )

    @property
    def url(self):
        return self.get_absolute_url().replace('/', '#', 1)

    @property
    def image_url_link(self):
        return {
            'menu_item': 'search',
            'name': 'search_tab_one_product' + str(self.pk),
            'link': self.get_absolute_url().replace('/', '#', 1),
            'image_url': self.image
        }

    def __str__(self):
        return self.productcode


class DimStore(models.Model, mixins_model.ModelFormFieldNames):
    id = models.IntegerField(primary_key=True)
    dim_channel = models.ForeignKey(DimChannel, on_delete=models.CASCADE, verbose_name='channel')
    dim_location = models.ForeignKey('DimLocation', models.DO_NOTHING, verbose_name='country code A2')
    store_code = models.CharField(unique=True, max_length=100)
    store_name = models.CharField(max_length=500, blank=True, null=True)
    store_display_label = models.CharField(max_length=500, blank=True, null=True)
    iln = models.CharField(verbose_name='ILN', max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    region_tax_rate = models.CharField(max_length=100, blank=True, null=True)
    local_currency = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    store_type = models.CharField(max_length=100, blank=True, null=True)
    store_location = models.CharField(max_length=100, blank=True, null=True)
    store_style = models.CharField(max_length=100, blank=True, null=True)
    customer_type = models.CharField(max_length=100, blank=True, null=True)
    potential = models.CharField(max_length=100, blank=True, null=True)
    store_size = models.FloatField(blank=True, null=True)
    store_tier = models.IntegerField(blank=True, null=True)

    form_field_list = [
        'id',
        'dim_channel',
        'store_type',
        'dim_location',
        'store_location',
        'store_code',
        'store_name',
        'store_display_label',
        'iln',
        'city',
        'region_tax_rate',
        'local_currency',
        'is_active',
        'store_style',
        'customer_type',
        'potential',
        'store_size',
        'store_tier',
    ]

    class Meta:
        verbose_name = 'Store'

    def get_store_active(self):
        if self.is_active:
            is_active
        return True

    def get_absolute_url(self):
        return reverse(
            'search_tab_one_store',
            kwargs={
                'pk': self.pk
            }
        )

    @property
    def url(self):
        return self.get_absolute_url().replace('/', '#', 1)

    @property
    def link(self):
        return {
            'menu_item': 'search',
            'name': 'search_tab_one_store' + str(self.pk),
            'link': self.get_absolute_url().replace('/', '#', 1),
        }


r"""
Fact tables connected to converted dim tables
"""

class FactMovements(models.Model):
    movementid = models.CharField(max_length=100, blank=True, null=True)
    movementdate = models.DateField()
    dim_date = models.ForeignKey(DimDate, on_delete=models.CASCADE)
    dim_store = models.ForeignKey(DimStore, on_delete=models.CASCADE)
    dim_product = models.ForeignKey(DimProduct, on_delete=models.CASCADE)
    movementtype = models.CharField(max_length=1, blank=True, null=True)
    units = models.IntegerField(blank=True, null=True)
    costvalue = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    salesvalue = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    movementnumber = models.CharField(max_length=100, blank=True, null=True)
    movementline = models.IntegerField(blank=True, null=True)
    insertdate = models.DateTimeField(blank=True, null=True)
    updatedate = models.DateTimeField(blank=True, null=True)
    insertsource = models.CharField(max_length=20, blank=True, null=True)
    updatesource = models.CharField(max_length=20, blank=True, null=True)

    # class Meta:
    #     indexes = [
    #         models.Index(fields=['movementdate', 'storeid', 'productid']),
    #     ]

class FactInventory(models.Model):
    inventorydate = models.DateField()
    storeid = models.ForeignKey(DimStore, on_delete=models.CASCADE)
    productid = models.ForeignKey(DimProduct, on_delete=models.CASCADE)
    unitonhand = models.IntegerField(blank=True, null=True)
    unitonorder = models.FloatField(blank=True, null=True)
    unitrequired = models.FloatField(blank=True, null=True)
    unitallocated = models.FloatField(blank=True, null=True)
    leadtime = models.FloatField(blank=True, null=True)
    unitprice = models.FloatField(blank=True, null=True)
    salesprice = models.FloatField(blank=True, null=True)
    minimumstocklevel = models.FloatField(blank=True, null=True)
    reorderlevel = models.FloatField(blank=True, null=True)
    excludedlevel = models.FloatField(blank=True, null=True)
    orderamount = models.FloatField(blank=True, null=True)
    orderlock = models.FloatField(blank=True, null=True)
    packsize = models.FloatField(blank=True, null=True)
    minimumorderquantity = models.FloatField(blank=True, null=True)
    safetylevel = models.FloatField(blank=True, null=True)
    totalsales = models.FloatField(blank=True, null=True)
    numbersales = models.FloatField(blank=True, null=True)
    paretostore = models.CharField(max_length=500, blank=True, null=True)
    paretoglobal = models.CharField(max_length=500, blank=True, null=True)
    replenishcode = models.CharField(max_length=500, blank=True, null=True)
    dcavailable = models.FloatField(blank=True, null=True)
    createdate = models.DateTimeField(blank=True, null=True)
    source = models.CharField(max_length=500, blank=True, null=True)
    supplierproductcode = models.FloatField(blank=True, null=True)

    # class Meta:
    #     indexes = [
    #         models.Index(fields=['inventorydate', 'storeid', 'productid']),
    #     ]




class DimIAPFilter(models.Model, mixins_model.ModelFormFieldNames):
    r'''
    Model for filter master
    '''
    dim_channel = models.ForeignKey(DimChannel, on_delete=models.CASCADE)
    sales_year = models.IntegerField()
    sales_season = models.CharField(max_length=2)

    form_field_list = [
        'id',
        'dim_channel',
        'sales_year',
        'sales_season',
    ]

    class Meta:
        verbose_name = 'IAP Filter'

    def get_label(self):
        return self.dim_channel.name + ' ' + str(self.sales_year) + ' ' + self.sales_season

    def __str__(self):
        return self.dim_channel.name + ' / ' + str(self.sales_year) + ' / ' + self.sales_season


class DimIAPFilterUser(models.Model, mixins_model.ModelFormFieldNames):
    r'''
    Model for filter master
    '''
    dim_iapfilter = models.ForeignKey(DimIAPFilter, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    form_field_list = [
        'id',
    ]

    class Meta:
        verbose_name = 'IAP Filter User'
        unique_together = (('dim_iapfilter', 'user'),)

    def __str__(self):
        return self.dim_channel.name


class DimIAPStep(models.Model, mixins_model.ModelFormFieldNames):
    r'''
    Model for channel master
    '''
    name = models.CharField(max_length=100)
    position = models.PositiveIntegerField(unique=True)

    form_field_list = [
        'id',
        'name',
        'position',
    ]

    class Meta:
        verbose_name = 'IAP Step'

    def __str__(self):
        return self.name

class DimIAPCycle(models.Model):
    r'''
    Model for storing an entire sales cycle
    '''
    dim_iapfilter = models.ForeignKey(DimIAPFilter, on_delete=models.CASCADE, default=1)
    dim_iapstep = models.ForeignKey(DimIAPStep, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completion_dt = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = (('dim_iapfilter', 'dim_iapstep'),)

r"""
Store clustering
"""
class FeatureStoreInput(models.Model, mixins_model.ModelFormFieldNames):
    r'''
    Model for machine learning clustering input
    '''
    # Unique fields
    id = models.AutoField(primary_key=True)
    dim_iapfilter = models.ForeignKey(DimIAPFilter, on_delete=models.CASCADE, default=1)
    dim_store = models.ForeignKey(DimStore, verbose_name='store code')

    # Additional fields
    net_retail_sales_in_eur_ty = models.FloatField(verbose_name='net sales TY (EUR)', blank=True, null=True)
    average_monthly_sales_for_ty = models.FloatField(verbose_name='average monthly sales TY (EUR)', blank=True, null=True)
    sku_count = models.IntegerField(verbose_name='SKU count', blank=True, null=True)
    relative_sales_volume_ty = models.FloatField(verbose_name='relative sales TY (EUR)', blank=True, null=True)
    average_value_transaction = models.FloatField(verbose_name='ASP (EUR)', blank=True, null=True)
    sales_swimwear = models.FloatField(verbose_name='net sales swimwear TY (EUR)', blank=True, null=True)
    sales_lingerie = models.FloatField(verbose_name='net sales lingerie TY (EUR)', blank=True, null=True)
    sales_legwear = models.FloatField(verbose_name='net sales legwear TY (EUR)', blank=True, null=True)
    sales_ready_to_wear = models.FloatField(verbose_name='net sales ready-to-wear TY (EUR)', blank=True, null=True)
    sales_accessories = models.FloatField(verbose_name='net sales accessories TY (EUR)', blank=True, null=True)
    sales_adv_promotion = models.FloatField(verbose_name='sales ADV promotion TY (EUR)', blank=True, null=True)

    # Fields for machine learning clustering output (as part of normal IAP flow)
    cluster_ai = models.CharField(verbose_name='cluster AI', max_length=2)
    cluster_user = models.CharField(max_length=2)
    optimal_assortment_similarity_coefficient = models.FloatField(blank=True, null=True)

    form_field_list = [
        'id',
        'cluster_ai',
        'cluster_user',
        'dim_store',
        'store name', # read only
        'store type', # read only
        'store size', # read only
        'region', # read only
        'country', # read only
        'net_retail_sales_in_eur_ty',
        # 'average_monthly_sales_for_ty',
        'relative_sales_volume_ty',
        'sku_count',
        'average_value_transaction',
        'sales_lingerie',
        'sales_legwear',
        'sales_ready_to_wear',
        'sales_accessories',
        'sales_swimwear',
        'sales_adv_promotion',
    ]

    class Meta:
        unique_together = (('dim_iapfilter', 'dim_store'),)



class FeatureStoreOutputSimulation(models.Model):
    r'''
    Model for machine learning clustering output (as part of simulation)
    '''

    # Unique fields
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feature = models.OneToOneField(
        FeatureStoreInput,
        on_delete=models.CASCADE,
    )

    # Additional fields
    cluster_ai = models.CharField(verbose_name='cluster AI', max_length=2)
    cluster_user = models.CharField(max_length=2)
    master_assortment_similarity_coefficient = models.FloatField(blank=True, null=True)

    class Meta:
        unique_together = (('feature', 'user'),)


class FeatureProductInputByCluster(models.Model, mixins_model.ModelFormFieldNames):
    r'''
    Model for master assortment creation input (by cluster)
    '''

    # Unique fields
    id = models.AutoField(primary_key=True)
    dim_iapfilter = models.ForeignKey(DimIAPFilter, on_delete=models.CASCADE, default=1)
    cluster = models.CharField(max_length=2)
    dim_product = models.ForeignKey(DimProduct)

    # Additional fields
    units = models.IntegerField(blank=True, null=True)
    salesvalueeur = models.FloatField(verbose_name='sales value (EUR)', blank=True, null=True)


    # Frontend display
    form_field_list = []

    class Meta:
        unique_together = (('dim_iapfilter', 'cluster', 'dim_product'),)


class FeatureProductInput(models.Model, mixins_model.ModelFormFieldNames):
    r'''
    Model for master assortment creation input
    '''

    # Unique fields
    id = models.AutoField(primary_key=True)
    dim_iapfilter = models.ForeignKey(DimIAPFilter, on_delete=models.CASCADE, default=1)
    dim_store = models.ForeignKey(DimStore)
    dim_product = models.ForeignKey(DimProduct)

    # Additional fields
    units = models.IntegerField(blank=True, null=True)
    salesvalueeur = models.FloatField(verbose_name='sales value (EUR)', blank=True, null=True)

    # Fields for master assortment creation output (as part of normal IAP flow)
    cluster_ai = models.CharField(verbose_name='cluster AI', max_length=2)
    cluster_user = models.CharField(max_length=2)

    # Frontend display
    form_field_list = [
        [
            'dim_product',
            [
                'productcode',
                'productshortdescription',
                'division',
                'category',
                'colour',
                'size',
            ]
        ],
        'cluster_ai',
        'cluster_user',
        'units',
        'salesvalueeur',
    ]

    class Meta:
        unique_together = (('dim_iapfilter', 'dim_store', 'dim_product'),)



class FeatureProductOutputSimulation(models.Model):
    r'''
    Model for master assortment creation output (as part of simulation)
    '''

    # Unique fields
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dim_product = models.ForeignKey(DimProduct)
    cluster_ai = models.CharField(verbose_name='cluster AI', max_length=2)
    cluster_user = models.CharField(max_length=2)

    # Additional fields
    units = models.IntegerField(blank=True, null=True)

    class Meta:
        unique_together = (('cluster_user', 'dim_product', 'user'),)


class FeatureImportanceOutputSimulation(models.Model):
    r'''
    Model for feature importance output (as part of simulation)
    '''

    # Unique fields
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    features = models.CharField(max_length=250)

    # Additional fields
    importance = models.FloatField(blank=True, null=True)

    class Meta:
        unique_together = (('user', 'features'),)


r"""
Sales planning
"""
class PlanByMonth(models.Model, mixins_model.ModelFormFieldNames):
    r'''
    Model for sales plan with configuration by month
    '''

    # Unique fields
    id = models.AutoField(primary_key=True)
    dim_iapfilter = models.ForeignKey(DimIAPFilter, on_delete=models.CASCADE, default=1)

    # Unique fields
    year_month_name_ly = models.CharField(verbose_name='month LY', max_length=7)

    # LY fields
    unit_sales_ly = models.IntegerField(verbose_name='unit sales LY', blank=True, null=True)
    value_sales_ly = models.FloatField(verbose_name='value sales LY', blank=True, null=True)

    # PY fields calculated
    year_month_name_py = models.CharField(verbose_name='month PY', max_length=7) # month_ly + 1 year
    unit_sales_py_product_category_level = models.IntegerField(verbose_name='unit sales PY brand', default=0, blank=True, null=True) # aggregated unit sales from PlanByProductCategory
    value_sales_py_product_category_level = models.FloatField(verbose_name='value sales PY brand', default=0, blank=True, null=True) # aggregated value sales from PlanByProductCategory
    unit_sales_py_store_level = models.IntegerField(verbose_name='unit sales PY retail', default=0, blank=True, null=True) # aggregated unit sales from PlanByStore
    value_sales_py_store_level = models.FloatField(verbose_name='value sales PY retail', default=0, blank=True, null=True) # aggregated value sales from PlanByStore

    # PY fields user input (but prefill from LY)
    unit_sales_py_year_month_level = models.IntegerField(verbose_name='units', default=0, blank=True, null=True)
    value_sales_py_year_month_level = models.FloatField(verbose_name='sales value', default=0, blank=True, null=True)

    # Frontend display
    form_field_list = [
        'id',
        'year_month_name_py',
        'unit_sales_py_year_month_level',
        'value_sales_py_year_month_level',
    ]

    class Meta:
        unique_together = (('dim_iapfilter', 'year_month_name_ly'),)


class PlanByProductCategory(models.Model, mixins_model.ModelFormFieldNames):
    r'''
    Model for sales plan with configuration by product category (month)
    '''

    # Unique fields
    id = models.AutoField(primary_key=True)
    dim_iapfilter = models.ForeignKey(DimIAPFilter, on_delete=models.CASCADE, default=1)

    # Unique fields
    product_category = models.CharField(verbose_name='product category', max_length=150)

    # Informative fields
    product_division = models.CharField(verbose_name='product group', max_length=150)

    # LY fields
    unit_sales_ly = models.IntegerField(verbose_name='unit sales LY', blank=True, null=True)
    value_sales_ly = models.FloatField(verbose_name='value sales LY', blank=True, null=True)

    # PY fields user input (but prefill from LY)
    unit_sales_py_index = models.FloatField(verbose_name='index', blank=True, null=True)
    unit_sales_py_mix = models.FloatField(verbose_name='mix', blank=True, null=True)

    # PY fields calculated
    unit_sales_py = models.IntegerField(verbose_name='unit sales PY', blank=True, null=True)
    value_sales_py = models.FloatField(verbose_name='value sales PY', blank=True, null=True)

    # Frontend display
    form_field_list = [
        'id',
        'product_category',
        'product_division',
        'unit_sales_ly',
        'value_sales_ly',
        'unit_sales_py_mix',
        'unit_sales_py_index',
        'unit_sales_py',
        'value_sales_py',
    ]

    class Meta:
        unique_together = (('dim_iapfilter', 'product_category'),)



class PlanByStore(models.Model, mixins_model.ModelFormFieldNames):
    r'''
    Model for sales plan with configuration by store
    '''

    # Unique fields
    id = models.AutoField(primary_key=True)
    dim_iapfilter = models.ForeignKey(DimIAPFilter, on_delete=models.CASCADE, default=1)

    # Unique fields
    store_code = models.CharField(unique=True, max_length=100)
    store_name = models.CharField(max_length=500, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    # Informative fields
    cluster_user = models.CharField(max_length=2)

    # LY fields
    unit_sales_ly = models.IntegerField(verbose_name='unit sales LY', blank=True, null=True)
    value_sales_ly = models.FloatField(verbose_name='value sales LY', blank=True, null=True)

    # PY fields user input (but prefill from LY)
    unit_sales_py_index = models.FloatField(verbose_name='index', blank=True, null=True)
    unit_sales_py_mix = models.FloatField(verbose_name='mix', blank=True, null=True)

    # PY fields calculated
    unit_sales_py = models.IntegerField(verbose_name='unit sales PY', blank=True, null=True)
    value_sales_py = models.FloatField(verbose_name='value sales PY', blank=True, null=True)

    # Frontend display
    form_field_list = [
        'id',
        'store_code',
        'cluster_user',
        'unit_sales_ly',
        'value_sales_ly',
        'unit_sales_py_mix',
        'unit_sales_py_index',
        'unit_sales_py',
        'value_sales_py',
    ]

    class Meta:
        unique_together = (('dim_iapfilter', 'store_code'),)



class PlanByMonthProductCategoryStore(models.Model):
    r'''
    Model for sales plan report by month, product category, store
    '''

    # Unique fields
    id = models.AutoField(primary_key=True)
    dim_iapfilter = models.ForeignKey(DimIAPFilter, on_delete=models.CASCADE, default=1)

    # Unique fields
    year_month_name_ly = models.CharField(verbose_name='month LY', max_length=7)
    dim_store = models.ForeignKey(DimStore, on_delete=models.CASCADE)
    product_category = models.CharField(verbose_name='product category', max_length=150)

    # Informative fields
    cluster_user = models.CharField(max_length=2)
    product_division = models.CharField(verbose_name='product group', max_length=150)
    year_month_name_py = models.CharField(verbose_name='month PY', max_length=7)

    # PY fields calculated
    unit_sales_py = models.IntegerField(verbose_name='unit sales PY', blank=True, null=True)
    value_sales_py = models.FloatField(verbose_name='value sales PY', blank=True, null=True)

    class Meta:
        unique_together = (('dim_iapfilter', 'year_month_name_ly', 'dim_store', 'product_category'),)


r"""
Range planning
"""
class RangeArchitecture(models.Model, mixins_model.ModelFormFieldNames):
    r'''
    Model for range architecture
    '''

    # Unique fields
    id = models.AutoField(primary_key=True)
    dim_iapfilter = models.ForeignKey(DimIAPFilter, on_delete=models.CASCADE, default=1)

    # Unique fields
    product_category = models.CharField(verbose_name='product category', max_length=150)

    # Informative fields
    product_division = models.CharField(verbose_name='product group', max_length=150)

    # range width - LY style level
    range_width_style_ly_essential_basic = models.IntegerField(verbose_name='range width style level LY essential basic', blank=True, null=True, default=0)
    range_width_style_ly_essential_fashion = models.IntegerField(verbose_name='range width style level LY essential fashion', blank=True, null=True, default=0)
    range_width_style_ly_trend_basic = models.IntegerField(verbose_name='range width style level LY trend basic', blank=True, null=True, default=0)
    range_width_style_ly_trend_fashion = models.IntegerField(verbose_name='range width style level LY trend fashion', blank=True, null=True, default=0)
    range_width_style_ly_total = models.IntegerField(verbose_name='style count LY', blank=True, null=True, default=0)

    # range width average colour count per style - LY style level (no display)
    range_width_style_ly_essential_basic_avg_colour_count = models.IntegerField(blank=True, null=True, default=0)
    range_width_style_ly_essential_fashion_avg_colour_count = models.IntegerField(blank=True, null=True, default=0)
    range_width_style_ly_trend_basic_avg_colour_count = models.IntegerField(blank=True, null=True, default=0)
    range_width_style_ly_trend_fashion_avg_colour_count = models.IntegerField(blank=True, null=True, default=0)

    # range width - PY style level
    range_width_style_py_carry_over = models.IntegerField(verbose_name='range width style level PY carry over', blank=True, null=True, default=0)
    range_width_style_py_essential_basic = models.IntegerField(verbose_name='range width style level PY essential basic', blank=True, null=True, default=0)
    range_width_style_py_essential_fashion = models.IntegerField(verbose_name='range width style level PY essential fashion', blank=True, null=True, default=0)
    range_width_style_py_trend_basic = models.IntegerField(verbose_name='range width style level PY trend basic', blank=True, null=True, default=0)
    range_width_style_py_trend_fashion = models.IntegerField(verbose_name='range width style level PY trend fashion', blank=True, null=True, default=0)
    range_width_style_py_total = models.IntegerField(verbose_name='style count PY', blank=True, null=True, default=0)

    # range width - LY style colour level
    range_width_style_colour_ly_essential_basic = models.IntegerField(verbose_name='range width style-colour level LY essential basic', blank=True, null=True, default=0)
    range_width_style_colour_ly_essential_fashion = models.IntegerField(verbose_name='range width style-colour level LY essential fashion', blank=True, null=True, default=0)
    range_width_style_colour_ly_trend_basic = models.IntegerField(verbose_name='range width style-colour level LY trend basic', blank=True, null=True, default=0)
    range_width_style_colour_ly_trend_fashion = models.IntegerField(verbose_name='range width style-colour level LY trend fashion', blank=True, null=True, default=0)
    range_width_style_colour_ly_total = models.IntegerField(verbose_name='style-colour count LY', blank=True, null=True, default=0)

    # range width - PY style colour level
    range_width_style_colour_py_carry_over = models.IntegerField(verbose_name='range width style-colour level PY carry over', blank=True, null=True, default=0)
    range_width_style_colour_py_essential_basic = models.IntegerField(verbose_name='range width style-colour level PY essential basic', blank=True, null=True, default=0)
    range_width_style_colour_py_essential_fashion = models.IntegerField(verbose_name='range width style-colour level PY essential fashion', blank=True, null=True, default=0)
    range_width_style_colour_py_trend_basic = models.IntegerField(verbose_name='range width style-colour level PY trend basic', blank=True, null=True, default=0)
    range_width_style_colour_py_trend_fashion = models.IntegerField(verbose_name='range width style-colour level PY trend fashion', blank=True, null=True, default=0)
    range_width_style_colour_py_total = models.IntegerField(verbose_name='style-colour count PY', blank=True, null=True, default=0)

    # range sales - LY (no display)
    range_sales_ly_essential_basic = models.IntegerField(verbose_name='range sales LY essential basic', blank=True, null=True, default=0)
    range_sales_ly_essential_fashion = models.IntegerField(verbose_name='range sales LY essential fashion', blank=True, null=True, default=0)
    range_sales_ly_trend_basic = models.IntegerField(verbose_name='range sales LY trend basic', blank=True, null=True, default=0)
    range_sales_ly_trend_fashion = models.IntegerField(verbose_name='range sales LY trend fashion', blank=True, null=True, default=0)
    range_sales_ly_total = models.IntegerField(verbose_name='range sales LY total', blank=True, null=True, default=0)

    # range effectiveness - LY
    range_effectiveness_style_ly_essential_basic = models.IntegerField(verbose_name='range effectiveness style level LY essential basic', blank=True, null=True, default=0)
    range_effectiveness_style_ly_essential_fashion = models.IntegerField(verbose_name='range effectiveness style level LY essential fashion', blank=True, null=True, default=0)
    range_effectiveness_style_ly_trend_basic = models.IntegerField(verbose_name='range effectiveness style level LY trend basic', blank=True, null=True, default=0)
    range_effectiveness_style_ly_trend_fashion = models.IntegerField(verbose_name='range effectiveness style level LY trend fashion', blank=True, null=True, default=0)
    range_effectiveness_style_ly_total = models.IntegerField(verbose_name='range effectiveness style level LY total', blank=True, null=True, default=0)

    # range effectiveness - PY
    range_effectiveness_style_py_carry_over = models.IntegerField(verbose_name='range effectiveness style level PY carry over', blank=True, null=True, default=0)
    range_effectiveness_style_py_essential_basic = models.IntegerField(verbose_name='range effectiveness style level PY essential basic', blank=True, null=True, default=0)
    range_effectiveness_style_py_essential_fashion = models.IntegerField(verbose_name='range effectiveness style level PY essential fashion', blank=True, null=True, default=0)
    range_effectiveness_style_py_trend_basic = models.IntegerField(verbose_name='range effectiveness style level PY trend basic', blank=True, null=True, default=0)
    range_effectiveness_style_py_trend_fashion = models.IntegerField(verbose_name='range effectiveness style level PY trend fashion', blank=True, null=True, default=0)
    range_effectiveness_style_py_total = models.IntegerField(verbose_name='range effectiveness style level PY total', blank=True, null=True, default=0)

    # range performance ASP LY
    range_performance_ly = models.IntegerField(verbose_name='ASP LY', blank=True, null=True, default=0)

    # range performance ASP PY
    range_performance_py = models.IntegerField(verbose_name='ASP PY', blank=True, null=True, default=0)

    # Frontend display
    form_field_list = [
        'product_division',
        'product_category',

        # range width - LY style level
        'range_width_style_ly_essential_basic',
        'range_width_style_ly_essential_fashion',
        'range_width_style_ly_trend_basic',
        'range_width_style_ly_trend_fashion',
        'range_width_style_ly_total',

        # range width - PY style level
        'range_width_style_py_carry_over',
        'range_width_style_py_essential_basic',
        'range_width_style_py_essential_fashion',
        'range_width_style_py_trend_basic',
        'range_width_style_py_trend_fashion',
        'range_width_style_py_total',

        # range width - LY style colour level
        'range_width_style_colour_ly_essential_basic',
        'range_width_style_colour_ly_essential_fashion',
        'range_width_style_colour_ly_trend_basic',
        'range_width_style_colour_ly_trend_fashion',
        'range_width_style_colour_ly_total',

        # range width - PY style colour level
        'range_width_style_colour_py_carry_over',
        'range_width_style_colour_py_essential_basic',
        'range_width_style_colour_py_essential_fashion',
        'range_width_style_colour_py_trend_basic',
        'range_width_style_colour_py_trend_fashion',
        'range_width_style_colour_py_total',

        # range effectiveness - LY
        'range_effectiveness_style_ly_essential_basic',
        'range_effectiveness_style_ly_essential_fashion',
        'range_effectiveness_style_ly_trend_basic',
        'range_effectiveness_style_ly_trend_fashion',
        'range_effectiveness_style_ly_total',

        # range effectiveness - PY
        'range_effectiveness_style_py_carry_over',
        'range_effectiveness_style_py_essential_basic',
        'range_effectiveness_style_py_essential_fashion',
        'range_effectiveness_style_py_trend_basic',
        'range_effectiveness_style_py_trend_fashion',
        'range_effectiveness_style_py_total',

        # range performance ASP LY
        'range_performance_ly',

        # range performance ASP TY
        'range_performance_py',
    ]

    class Meta:
        unique_together = (('dim_iapfilter', 'product_category'),)


class RangeMaster(models.Model, mixins_model.ModelFormFieldNames):
    r'''
    Model for range architecture
    '''

    # Unique fields
    id = models.AutoField(primary_key=True)
    dim_iapfilter = models.ForeignKey(DimIAPFilter, on_delete=models.CASCADE, default=1)

    # Unique fields
    model_number = models.CharField(max_length=100)
    style_number = models.CharField(max_length=100)
    colour_number = models.CharField(max_length=100)

    # Attribute fields
    product_division = models.CharField(verbose_name='product group', max_length=150)
    product_category = models.CharField(verbose_name='product category', max_length=150)
    product_essential_trend = models.CharField(verbose_name='essential trend', max_length=100, blank=True, null=True)
    product_basic_fashion = models.CharField(verbose_name='basic fashion', max_length=100, blank=True, null=True)
    model_name = models.CharField(max_length=100)
    style_name = models.CharField(max_length=100, blank=True, null=True)
    colour_name = models.CharField(max_length=100, blank=True, null=True)
    material = models.CharField(max_length=100, blank=True, null=True)

    # Frontend display
    form_field_list = [
        'id',
        'model_number',
        'model_name',
        'style_number',
        'style_name',
        'colour_number',
        'colour_name',
        'product_division',
        'product_category',
        'product_essential_trend',
        'product_basic_fashion',
        'material',
    ]

    class Meta:
        unique_together = (('dim_iapfilter', 'model_number', 'style_number', 'colour_number'),)


# class StagingRangePlan(models.Model):
#     product_group = models.BigIntegerField(blank=True, null=True)
#     product_essential_trend = models.TextField(blank=True, null=True)
#     product_basic_fashion = models.TextField(blank=True, null=True)
#     product_category = models.TextField(blank=True, null=True)
#     style_colour_x = models.FloatField(blank=True, null=True)
#     style = models.BigIntegerField(blank=True, null=True)
#     style_colour_y = models.BigIntegerField(blank=True, null=True)
#
#     class Meta:
#         managed = False


# r"""
# Buy planning
# """
# class DimMarkup(models.Model):
#     country = models.CharField(max_length=500, blank=True, null=True)
#     category = models.CharField(max_length=500, blank=True, null=True)
#     markup = models.FloatField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#
#
# class StagingBuyPlan(models.Model):
#     product_group = models.CharField(max_length=500, blank=True, null=True)
#     trend_ess = models.CharField(max_length=500, blank=True, null=True)
#     bc_fc = models.CharField(max_length=500, blank=True, null=True)
#     article_no = models.CharField(max_length=500, blank=True, null=True)
#     style_name = models.CharField(max_length=500, blank=True, null=True)
#     classification = models.CharField(max_length=500, blank=True, null=True)
#     colour_name = models.CharField(max_length=500, blank=True, null=True)
#     pgfascol = models.CharField(max_length=500, blank=True, null=True)
#     delivery = models.IntegerField(blank=True, null=True)
#     as400_collection_date = models.IntegerField(blank=True, null=True)
#     delivery_date = models.CharField(max_length=500, blank=True, null=True)
#     banding_grading = models.CharField(max_length=500, blank=True, null=True)
#     rrp_in_eur = models.FloatField(blank=True, null=True)
#     rrp_net = models.FloatField(blank=True, null=True)
#     available_size_run = models.CharField(max_length=500, blank=True, null=True)
#     lookup = models.CharField(max_length=500, blank=True, null=True)
#     ean_code = models.BigIntegerField(blank=True, null=True)
#     total_global_apl = models.FloatField(blank=True, null=True)
#     retail_buy_units_style = models.IntegerField(blank=True, null=True)
#     percentage_sbd = models.FloatField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#
#
# class StagingOtbHighLevelInput(models.Model):
#     region = models.CharField(max_length=500, blank=True, null=True)
#     parameter_type = models.CharField(max_length=500, blank=True, null=True)
#     parameter_name = models.CharField(max_length=500, blank=True, null=True)
#     value = models.FloatField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#
#
# class StagingOtbProductGroupLevelInput(models.Model):
#     region = models.CharField(max_length=500, blank=True, null=True)
#     product_group = models.CharField(max_length=500, blank=True, null=True)
#     season = models.CharField(max_length=500, blank=True, null=True)
#     fashion_mix = models.FloatField(blank=True, null=True)
#     trend_mix = models.FloatField(blank=True, null=True)
#     discount_rate = models.FloatField(blank=True, null=True)
#     after_sale_sellthru = models.FloatField(blank=True, null=True)
#     before_sale_sellthru = models.FloatField(blank=True, null=True)
#     discount_in_sale = models.FloatField(blank=True, null=True)
#     markup_rate = models.FloatField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#
#
# class StagingBudgetMarketLevelInput(models.Model):
#     year = models.IntegerField(blank=True, null=True)
#     currency = models.CharField(max_length=500, blank=True, null=True)
#     country = models.CharField(max_length=500, blank=True, null=True)
#     market = models.CharField(max_length=500, blank=True, null=True)
#     region = models.CharField(max_length=500, blank=True, null=True)
#     wbo = models.IntegerField(blank=True, null=True)
#     siso = models.IntegerField(blank=True, null=True)
#     coaff = models.FloatField(blank=True, null=True)
#     fo = models.IntegerField(blank=True, null=True)
#     b2c_fp = models.IntegerField(blank=True, null=True)
#     b2c_fo = models.IntegerField(blank=True, null=True)
#
#     class Meta:
#         managed = False


r"""
Strategic Sales Plan
"""
class StrategicSalesPlan(models.Model, mixins_model.ModelFormFieldNames):
    r'''
    Model for strategic sales plan
    '''

    # Unique fields
    id = models.AutoField(primary_key=True)
    dim_channel = models.ForeignKey(DimChannel, on_delete=models.CASCADE, default=1)
    sales_year = models.IntegerField(default=2017)
    sales_season = models.CharField(default='SS', max_length=2)

    # Unique fields
    region = models.CharField(max_length=45)
    scenario = models.CharField(default='conservative', max_length=45)

    # Level specific fields
    gross_sales_index = models.FloatField(default=1, blank=True, null=True)
    seasonal_mix = models.FloatField(default=0, blank=True, null=True)
    channel_mix = models.FloatField(default=0, blank=True, null=True)

    # Informative fields
    gross_sales = models.FloatField(default=0, blank=True, null=True)
    gross_sales_init = models.FloatField(default=0, blank=True, null=True)
    asp = models.FloatField(default=0, blank=True, null=True)
    gross_sales_per_unit = models.IntegerField(default=0, blank=True, null=True)
    discounts = models.FloatField(default=0, blank=True, null=True)
    returns = models.FloatField(default=0, blank=True, null=True)
    net_sales = models.FloatField(default=0, blank=True, null=True)
    sell_through_ratio = models.FloatField(default=0, blank=True, null=True)
    sell_in = models.FloatField(default=0, blank=True, null=True)
    markup = models.FloatField(default=0, blank=True, null=True)
    gross_margin_percentage = models.FloatField(default=0, blank=True, null=True)
    gross_margin = models.FloatField(default=0, blank=True, null=True)
    buying_budget = models.FloatField(default=0, blank=True, null=True)
    gmroi_percentage_target = models.FloatField(default=0, blank=True, null=True)
    beginning_season_inventory = models.FloatField(default=0, blank=True, null=True)
    ending_season_inventory = models.FloatField(default=0, blank=True, null=True)
    markdown = models.FloatField(default=0, blank=True, null=True)
    row_styling = models.CharField(max_length=45, blank=True, null=True)
    average_cost_of_inventory = models.FloatField(default=0, blank=True, null=True)
    intake_beginning_of_season = models.FloatField(default=0, blank=True, null=True)

    # Frontend display
    form_field_list = [
        'region',
    ]

    class Meta:
        unique_together = (('dim_channel', 'sales_year', 'sales_season', 'region', 'scenario'),)


class FactSalesForecast(models.Model):
    dim_date = models.ForeignKey(DimDate, on_delete=models.CASCADE)
    dim_store = models.ForeignKey(DimStore, on_delete=models.CASCADE)
    dim_product = models.ForeignKey(DimProduct, on_delete=models.CASCADE)
    units = models.IntegerField(blank=True, null=True)
    fitted = models.IntegerField(blank=True, null=True)
    rmse = models.IntegerField(blank=True, null=True)
    overwritten = models.IntegerField(blank=True, null=True)
    user_name = models.CharField(max_length=100, blank=True, null=True)
    is_locked = models.IntegerField(blank=True, null=True)

    class Meta:
        unique_together = (('dim_date', 'dim_store', 'dim_product'),)
