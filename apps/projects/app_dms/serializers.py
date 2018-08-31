from rest_framework import serializers

from . import models
from . import mixins_serializer
from core import utils


class DimStoreSerializer(
    mixins_serializer.DimLocationLookup,
    mixins_serializer.DimChannelLookup,
    mixins_serializer.IsActiveLookup,
    serializers.ModelSerializer
):
    r"""
    Serializer for master table
    """

    # Read-only fields
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.DimStore
        fields = (
            'id',
            'dim_channel', 'dim_channel_read_only', # Write and read only fields
            'store_type',
            'dim_location', 'dim_location_read_only', # Write and read only fields
            'store_location',
            'store_code',
            'store_name',
            'store_display_label',
            'iln',
            'city',
            'region_tax_rate',
            'local_currency',
            'is_active', 'is_active_read_only', # Write and read only fields
            'store_style',
            'customer_type',
            'potential',
            'store_size',
            'store_tier',
        )


class FeatureStoreInputSerializer(
    # mixins_serializer.DimLocationLookup,
    # mixins_serializer.IsActiveLookup,
    # mixins_serializer.DimStoreLookup,
    serializers.ModelSerializer
):
    r"""
    Serializer for master table
    """

    # Read-only fields
    id = serializers.IntegerField(read_only=True)
    cluster_user_read_only = serializers.SerializerMethodField()
    cluster_ai_read_only = serializers.SerializerMethodField()
    dim_store_code_read_only = serializers.SerializerMethodField()
    dim_store_name_read_only = serializers.SerializerMethodField()
    dim_store_type_read_only = serializers.SerializerMethodField()
    dim_store_size_read_only = serializers.SerializerMethodField()
    dim_store_region_read_only = serializers.SerializerMethodField()
    dim_store_country_read_only = serializers.SerializerMethodField()
    net_retail_sales_in_eur_ty_read_only = serializers.SerializerMethodField()
    # average_monthly_sales_for_ty_read_only = serializers.SerializerMethodField()
    sku_count_read_only = serializers.SerializerMethodField()
    average_value_transaction_read_only = serializers.SerializerMethodField()
    sales_lingerie_read_only = serializers.SerializerMethodField()
    sales_legwear_read_only = serializers.SerializerMethodField()
    sales_ready_to_wear_read_only = serializers.SerializerMethodField()
    sales_accessories_read_only = serializers.SerializerMethodField()
    sales_swimwear_read_only = serializers.SerializerMethodField()
    sales_adv_promotion_read_only = serializers.SerializerMethodField()

    # Write-only fields
    cluster_user = serializers.CharField(write_only=True)

    # Read-only methods (get_ is a DRF prefix)
    def get_cluster_user_read_only(self, obj):
        return obj.cluster_user

    def get_cluster_ai_read_only(self, obj):
        return obj.cluster_ai

    def get_dim_store_code_read_only(self, obj):
        return obj.dim_store.store_code

    def get_dim_store_name_read_only(self, obj):
        return obj.dim_store.store_name

    def get_dim_store_type_read_only(self, obj):
        return obj.dim_store.store_type

    def get_dim_store_size_read_only(self, obj):
        return obj.dim_store.store_size

    def get_dim_store_region_read_only(self, obj):
        return obj.dim_store.dim_location.region

    def get_dim_store_country_read_only(self, obj):
        return obj.dim_store.dim_location.country

    def get_net_retail_sales_in_eur_ty_read_only(self, obj):
        return obj.net_retail_sales_in_eur_ty

    # def get_average_monthly_sales_for_ty_read_only(self, obj):
    #     return obj.average_monthly_sales_for_ty

    def get_sku_count_read_only(self, obj):
        return obj.sku_count

    def get_average_value_transaction_read_only(self, obj):
        return obj.average_value_transaction

    def get_sales_lingerie_read_only(self, obj):
        return obj.sales_lingerie

    def get_sales_legwear_read_only(self, obj):
        return obj.sales_legwear

    def get_sales_ready_to_wear_read_only(self, obj):
        return obj.sales_ready_to_wear

    def get_sales_adv_promotion_read_only(self, obj):
        return obj.sales_adv_promotion

    def get_sales_accessories_read_only(self, obj):
        return obj.sales_accessories

    def get_sales_swimwear_read_only(self, obj):
        return obj.sales_swimwear

    # Validation rules
    def validate_cluster_user(self, value):
        value = value[:1].upper()
        valid_values = models.FeatureStoreInput.objects.values_list(
              'cluster_ai',
              flat=True
        ).order_by('cluster_ai').distinct()
        if value in valid_values:
            return value
        raise serializers.ValidationError('Value must be one of the following: ' + ', '.join(map(str, valid_values)))

    class Meta:
        model = models.FeatureStoreInput
        fields = (
            'id',
            'cluster_ai_read_only',
            'cluster_user', 'cluster_user_read_only', # Write and read only fields
            'dim_store_code_read_only', # read only fields
            'dim_store_name_read_only', # read only fields
            'dim_store_type_read_only', # read only fields
            'dim_store_size_read_only', # read only fields
            'dim_store_region_read_only', # read only fields
            'dim_store_country_read_only', # read only fields
            'net_retail_sales_in_eur_ty_read_only',
            # 'average_monthly_sales_for_ty_read_only',
            'sku_count_read_only',
            'average_value_transaction_read_only',
            'sales_lingerie_read_only',
            'sales_legwear_read_only',
            'sales_ready_to_wear_read_only',
            'sales_accessories_read_only',
            'sales_swimwear_read_only',
            'sales_adv_promotion_read_only',
        )


class PlanByMonthSerializer(
    serializers.ModelSerializer
):
    r"""
    Serializer for master table
    """

    # Read-only fields
    id = serializers.IntegerField(read_only=True)

    # Validation rules
    # def validate_cluster_user(self, value):
    #     model_item = models.FeatureStoreInput.objects.filter(name=value)
    #     if model_item.count() > 0:
    #         return model_item.first()
    #     raise serializers.ValidationError('Value must exist in channel master')

    class Meta:
        model = models.PlanByMonth
        fields = model.get_form_field_names_tuple(model)


class PlanByProductCategorySerializer(
    serializers.ModelSerializer
):
    r"""
    Serializer for master table
    """

    # Read-only fields
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.PlanByProductCategory
        fields = model.get_form_field_names_tuple(model)


class DimLocationSerializer(
    mixins_serializer.RegionLookup,
    serializers.ModelSerializer
):
    r"""
    Serializer for master table
    """

    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.DimLocation
        fields = model.get_form_field_names_tuple(model)


class DimChannelSerializer(
    serializers.ModelSerializer
):
    r"""
    Serializer for master table
    """

    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.DimChannel
        fields = model.get_form_field_names_tuple(model)


class RangeMasterSerializer(
    serializers.ModelSerializer
):
    r"""
    Serializer for master table
    """

    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.RangeMaster
        fields = model.get_form_field_names_tuple(model)

    # Validation rules
    def validate(self, data):
        model_item = models.DimProduct.objects.filter(category__icontains=data['product_category'])
        if model_item.count() > 0:
            data['product_category'] = model_item.first().category
            data['product_division'] = models.DimProduct.objects.filter(category=data['product_category']).first().division
            return data
        raise serializers.ValidationError('Product category must exist in product master (or at least have a similar value existing).')


class SizeCurveSerializer(
    serializers.ModelSerializer
):
    r"""
    Serializer for master table
    """

    # Read-only fields
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.SizeCurve
        fields = model.get_form_field_names_tuple(model)

    # Validation rules
    def validate(self, data):
        model_item = models.DimProduct.objects.filter(category__icontains=data['product_category'])
        if model_item.count() > 0:
            data['product_category'] = model_item.first().category
            data['product_division'] = models.DimProduct.objects.filter(category=data['product_category']).first().division
        else:
            raise serializers.ValidationError('Product category must exist in product master (or at least have a similar value existing).')

        data['xs'] = round(data['xs'], 2)
        data['s'] = round(data['s'], 2)
        data['m'] = round(data['m'], 2)
        data['l'] = round(data['l'], 2)
        data['xl'] = round(data['xl'], 2)
        size_sum = round(data['xs'] + data['s'] + data['m'] + data['l'] + data['xl'], 2)
        if size_sum == 1:
            return data
        else:
            raise serializers.ValidationError('Sum of all sizes must be 1 (= 100%). Current sum is ' + str(size_sum))
