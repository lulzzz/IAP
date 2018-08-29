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
    dim_iapfilter = models.ForeignKey(DimIAPFilter, on_delete=models.CASCADE, default=1, verbose_name='IAP Filter')
    dim_iapstep = models.ForeignKey(DimIAPStep, on_delete=models.CASCADE, verbose_name='IAP Step')
    is_completed = models.BooleanField(default=False, verbose_name='Status')
    completion_dt = models.DateTimeField(blank=True, null=True, verbose_name='Completion Date')

    class Meta:
        verbose_name = 'IAP Cycle'
        unique_together = (('dim_iapfilter', 'dim_iapstep'),)

    def __str__(self):
        return self.dim_iapfilter.dim_channel.name + ' ' + \
        str(self.dim_iapfilter.sales_year) + ' ' + \
        self.dim_iapfilter.sales_season + ' ' + \
        ' -> Step ' + str(self.dim_iapstep.position)

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


class RangePlan(models.Model, mixins_model.ModelFormFieldNames):
    r'''
    Model for range architecture
    '''

    # Unique fields
    id = models.AutoField(primary_key=True)

    # Unique fields
    dim_iapfilter = models.ForeignKey(DimIAPFilter, on_delete=models.CASCADE, default=1)
    product_category = models.CharField(verbose_name='product category', max_length=150)
    product_essential_trend = models.CharField(verbose_name='essential trend', max_length=100, blank=True, null=True)
    product_basic_fashion = models.CharField(verbose_name='basic fashion', max_length=100, blank=True, null=True)

    # Attribute fields
    product_division = models.CharField(verbose_name='product group', max_length=150)

    # From range architecture
    range_width_style_py_rangearchitecture = models.IntegerField(verbose_name='# of style codes from range architecture', blank=True, null=True, default=0)
    range_width_style_colour_py_rangearchitecture = models.IntegerField(verbose_name='# of style-colour codes from range architecture', blank=True, null=True, default=0)

    # From ERP (range master handsontable)
    range_width_style_py_rangemaster = models.IntegerField(verbose_name='# of style codes from range master', blank=True, null=True, default=0)
    range_width_style_colour_py_rangemaster = models.IntegerField(verbose_name='# of style-colour codes from range master', blank=True, null=True, default=0)

    # Frontend display
    form_field_list = [
        'product_division',
        'product_category',
        'product_essential_trend',
        'product_basic_fashion',

        'range_width_style_py_rangearchitecture',
        'range_width_style_colour_py_rangearchitecture',
        'range_width_style_py_rangemaster',
        'range_width_style_colour_py_rangemaster',
    ]

    class Meta:
        unique_together = (('dim_iapfilter', 'product_category', 'product_essential_trend', 'product_basic_fashion'),)


class RangeAssortment(models.Model, mixins_model.ModelFormFieldNames):
    r'''
    Model for range architecture
    '''

    # Unique fields
    id = models.AutoField(primary_key=True)

    # Unique fields
    dim_iapfilter = models.ForeignKey(DimIAPFilter, on_delete=models.CASCADE, default=1)
    cluster_user = models.CharField(verbose_name='cluster', max_length=2)
    product_category = models.CharField(verbose_name='product category', max_length=150)
    product_essential_trend = models.CharField(verbose_name='essential trend', max_length=100, blank=True, null=True)
    product_basic_fashion = models.CharField(verbose_name='basic fashion', max_length=100, blank=True, null=True)

    # Attribute fields
    product_division = models.CharField(verbose_name='product group', max_length=150)

    # From range architecture (LY)
    range_width_style_ly_storecluster = models.IntegerField(verbose_name='# of style codes LY from store clustering', blank=True, null=True, default=0)
    range_width_style_colour_ly_storecluster = models.IntegerField(verbose_name='# of style-colour codes LY from store clustering', blank=True, null=True, default=0)

    # User input (PY)
    range_width_style_py = models.IntegerField(verbose_name='# of style codes PY', blank=True, null=True, default=0)
    range_width_style_colour_py = models.IntegerField(verbose_name='# of style-colour codes PY', blank=True, null=True, default=0)

    # Frontend display
    form_field_list = [
        'cluster_user',
        'product_division',
        'product_category',
        'product_essential_trend',
        'product_basic_fashion',

        'range_width_style_ly_storecluster',
        'range_width_style_colour_ly_storecluster',
        'range_width_style_py',
        'range_width_style_colour_py',
    ]

    class Meta:
        unique_together = (('dim_iapfilter', 'cluster_user', 'product_category', 'product_essential_trend', 'product_basic_fashion'),)


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


# r"""
# Buy planning
# """
class SizeCurve(models.Model, mixins_model.ModelFormFieldNames):
    r'''
    Model for buy plan
    '''
    # Unique fields
    id = models.AutoField(primary_key=True)

    # Unique fields
    dim_iapfilter = models.ForeignKey(DimIAPFilter, on_delete=models.CASCADE, default=8)
    product_category = models.CharField(verbose_name='product category', max_length=150)

    # Attribute fields
    product_division = models.CharField(verbose_name='product group', max_length=150)

    # SIZE CURVE
    xs = models.FloatField(verbose_name='size curve XS', blank=True, null=True, default=0.1)
    s = models.FloatField(verbose_name='size curve S', blank=True, null=True, default=0.2)
    m = models.FloatField(verbose_name='size curve M', blank=True, null=True, default=0.3)
    l = models.FloatField(verbose_name='size curve L', blank=True, null=True, default=0.3)
    xl = models.FloatField(verbose_name='size curve XL', blank=True, null=True, default=0.1)

    # Frontend display
    form_field_list = [
        'id',
        'product_division',
        'product_category',
        'xs',
        's',
        'm',
        'l',
        'xl',
    ]

    class Meta:
        unique_together = (('dim_iapfilter', 'product_category'),)



class BuyPlan(models.Model, mixins_model.ModelFormFieldNames):
    r'''
    Model for buy plan
    '''

    # Unique fields
    id = models.AutoField(primary_key=True)

    # Unique fields
    dim_iapfilter = models.ForeignKey(DimIAPFilter, on_delete=models.CASCADE, default=1)
    cluster_user = models.CharField(verbose_name='cluster', max_length=2)
    product_category = models.CharField(verbose_name='product category', max_length=150)
    product_style = models.CharField(max_length=150, default='Style 1')
    product_essential_trend = models.CharField(verbose_name='essential trend', max_length=100, blank=True, null=True)
    product_basic_fashion = models.CharField(verbose_name='basic fashion', max_length=100, blank=True, null=True)
    # product_carryover = models.CharField(verbose_name='carry over', max_length=100, blank=True, null=True)

    # Attribute fields
    product_division = models.CharField(verbose_name='product group', max_length=150)

    # PRICING
    pricing_cost = models.IntegerField(verbose_name='cost', blank=True, null=True, default=0)
    pricing_selling_price = models.IntegerField(verbose_name='selling price', blank=True, null=True, default=0)

    # RANGE WIDTH
    range_width_style_colour_py = models.IntegerField(verbose_name='# of style-colour codes PY', blank=True, null=True, default=0)

    # QUANTITY TO BUY
    line_life_in_weeks = models.IntegerField(blank=True, null=True, default=0)
    rate_of_sales = models.FloatField(blank=True, null=True, default=0)
    number_of_stores = models.IntegerField(blank=True, null=True, default=0)
    targeted_sell_thru = models.FloatField(verbose_name='targeted sell thru %', blank=True, null=True, default=0)
    quantity_to_buy = models.IntegerField(blank=True, null=True, default=0)

    # OTB
    otc_quantity = models.IntegerField(verbose_name='OTB quantity', blank=True, null=True, default=0)

    # RANGE DEPTH BY STYLE BY COLOUR
    range_effectiveness_style_colour_py = models.IntegerField(verbose_name='range effectiveness', blank=True, null=True, default=0)

    # SIZE CURVE
    size_curve_xs = models.IntegerField(verbose_name='size curve XS', blank=True, null=True, default=0)
    size_curve_s = models.IntegerField(verbose_name='size curve S', blank=True, null=True, default=0)
    size_curve_m = models.IntegerField(verbose_name='size curve M', blank=True, null=True, default=0)
    size_curve_l = models.IntegerField(verbose_name='size curve L', blank=True, null=True, default=0)
    size_curve_xl = models.IntegerField(verbose_name='size curve XL', blank=True, null=True, default=0)

    # Frontend display
    form_field_list = [
        'cluster_user',
        'product_division',
        'product_category',
        'product_style',
        'product_essential_trend',
        'product_basic_fashion',

        'pricing_cost',
        'pricing_selling_price',
        'range_width_style_colour_py',
        'line_life_in_weeks',
        'rate_of_sales',
        'number_of_stores',
        'targeted_sell_thru',
        'quantity_to_buy',
        'otc_quantity',
        'range_effectiveness_style_colour_py',
        'size_curve_xs',
        'size_curve_s',
        'size_curve_m',
        'size_curve_l',
        'size_curve_xl',
    ]

    class Meta:
        unique_together = (('dim_iapfilter', 'cluster_user', 'product_category', 'product_style', 'product_essential_trend', 'product_basic_fashion'),)


class OTBPlanSupport(models.Model, mixins_model.ModelFormFieldNames):
    r'''
    Model for OTB plan supporting table
    '''

    # Unique fields
    id = models.AutoField(primary_key=True)

    # Unique fields
    dim_iapfilter = models.ForeignKey(DimIAPFilter, on_delete=models.CASCADE, default=1)
    region = models.CharField(max_length=45)

    # SALES
    net_sales = models.IntegerField(default=0)
    trade_product_sales = models.IntegerField(default=0)
    total_sales = models.IntegerField(default=0)
    average_vat_percentage = models.FloatField(verbose_name='average VAT %',default=0)
    average_vat = models.IntegerField(verbose_name='average VAT', default=0)
    gross_sales = models.IntegerField(default=0)

    # Frontend display
    form_field_list = [
        'region',
        'net_sales',
        'trade_product_sales',
        'total_sales',
        'average_vat_percentage',
        'average_vat',
        'gross_sales',
    ]

    class Meta:
        unique_together = (('dim_iapfilter', 'region',),)


class OTBPlanMix(models.Model, mixins_model.ModelFormFieldNames):
    r'''
    Model for OTB plan mix table
    '''

    # Unique fields
    id = models.AutoField(primary_key=True)

    # Unique fields
    dim_iapfilter = models.ForeignKey(DimIAPFilter, on_delete=models.CASCADE, default=1)
    region = models.CharField(max_length=45)
    product_type = models.CharField(verbose_name='product type', max_length=100)


    # MIX AND EUR
    mix = models.FloatField(default=0)
    value = models.IntegerField(verbose_name='EUR', default=0)

    # Frontend display
    form_field_list = [
        'region',
        'product_type',
        'mix',
        'value',
    ]

    class Meta:
        unique_together = (('dim_iapfilter', 'region', 'product_type',),)


class OTBPlan(models.Model, mixins_model.ModelFormFieldNames):
    r'''
    Model for OTB plan
    '''

    # Unique fields
    id = models.AutoField(primary_key=True)

    # Unique fields
    dim_iapfilter = models.ForeignKey(DimIAPFilter, on_delete=models.CASCADE, default=1)
    region = models.CharField(max_length=45)
    product_division = models.CharField(verbose_name='product group', max_length=150)

    # ESSENTIAL FASHION
    net_sales_essential_fashion_py = models.IntegerField(verbose_name='net sales essential fashion', default=0)
    mix_essential_fashion_py = models.FloatField(verbose_name='essential fashion mix PY', default=0)
    mix_essential_fashion_ly = models.FloatField(verbose_name='essential fashion mix LY', default=0)

    # TREND
    net_sales_trend_py = models.IntegerField(verbose_name='net sales trend', default=0)
    mix_trend_py = models.FloatField(verbose_name='trend mix PY', default=0)
    mix_trend_ly = models.FloatField(verbose_name='trend mix LY', default=0)

    # ESSENTIAL FASHION + TREND
    net_sales_essential_fashion_and_trend_py = models.IntegerField(verbose_name='net sales essential fashion and trend', default=0)
    average_discount_rate = models.FloatField(default=0)
    total_discount = models.IntegerField(default=0)
    gross_sales_essential_fashion_and_trend_py = models.IntegerField(verbose_name='gross sales essential fashion and trend', default=0)

    # RATES
    after_sale_sellthru_rate = models.FloatField(default=0)
    before_sale_sellthru_rate = models.FloatField(default=0)
    discount_in_sale_rate = models.FloatField(default=0)

    # SELL IN FULL PRICE
    sell_in_full_price = models.IntegerField(default=0)

    # YELLOW CALCULATIONS
    insale_net_sales = models.IntegerField(default=0)
    net_sales_sale = models.IntegerField(default=0)
    discount_in_sale = models.IntegerField(default=0)
    difference_in_discount = models.IntegerField(default=0)

    # BUYING BUDGET
    end_of_season_inventory = models.IntegerField(default=0)
    total_sell_in = models.IntegerField(verbose_name='total sell-in', default=0)
    markup_rate = models.FloatField(verbose_name='mark-up rate', default=0)
    total_buying_budget = models.IntegerField(default=0)
    average_vat_percentage = models.FloatField(verbose_name='average VAT %', default=0)
    total_buying_budget_adjusted_for_vat = models.IntegerField(verbose_name='total buying budget adjusted for VAT', default=0)

    # Frontend display
    form_field_list = [
        'region',
        'product_division',

        # ESSENTIAL FASHION + TREND
        'net_sales_essential_fashion_py',
        'net_sales_trend_py',
        'mix_essential_fashion_py',
        'mix_trend_py',
        'mix_essential_fashion_ly',
        'mix_trend_ly',
        'net_sales_essential_fashion_and_trend_py',
        'average_discount_rate',
        'total_discount',
        'gross_sales_essential_fashion_and_trend_py',

        # RATES
        'after_sale_sellthru_rate',
        'before_sale_sellthru_rate',
        'discount_in_sale_rate',
        'sell_in_full_price',

        # BUYING BUDGET
        'end_of_season_inventory',
        'total_sell_in',
        'markup_rate',
        'total_buying_budget',
        'average_vat_percentage',
        'total_buying_budget_adjusted_for_vat',
    ]

    class Meta:
        unique_together = (('dim_iapfilter', 'region', 'product_division',),)


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
    sales_year_mix = models.FloatField(default=0, blank=True, null=True)

    # Informative fields
    row_styling = models.CharField(max_length=45, blank=True, null=True)
    gross_sales = models.FloatField(default=0, blank=True, null=True)
    gross_sales_init = models.FloatField(default=0, blank=True, null=True)
    asp = models.FloatField(default=0, blank=True, null=True)
    sales_units_init = models.IntegerField(default=0, blank=True, null=True)
    sales_units = models.IntegerField(default=0, blank=True, null=True)
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
