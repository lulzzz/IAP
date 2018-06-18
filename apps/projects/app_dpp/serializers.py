from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from . import models
from . import mixins_serializer
from core import utils


class DimCustomerSerializer(
    mixins_serializer.DimLocationLookup,
    mixins_serializer.IsActiveLookup,
    mixins_serializer.IsPlaceholderLookup,
    serializers.ModelSerializer
):
    r"""
    Serializer for master table
    """

    # Read-only fields
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.DimCustomer
        fields = (
            'id',
            'dim_location', 'dim_location_read_only', # Write and read only fields
            'name',
            'market',
            'dc_plt',
            'sold_to_party',
            'sold_to_category',
            'is_active', 'is_active_read_only', # Write and read only fields
            'is_placeholder', 'is_placeholder_read_only', # Write and read only fields
            'placeholder_level',
        )


class DimProductionLineSerializer(
    mixins_serializer.DimFactoryLookup,
    serializers.ModelSerializer
):
    r"""
    Serializer for master table
    """

    # Read-only fields
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.DimProductionLine
        fields = (
            'id',
            'dim_factory', 'dim_factory_read_only', # Write and read only fields
            'line',
        )


class DimFactorySerializer(
    mixins_serializer.DimLocationLookup,
    mixins_serializer.IsActiveLookup,
    serializers.ModelSerializer
):

    # Read-only fields
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.DimFactory
        fields = (
            'id',
            'plant_code',
            'vendor_code',
            'vendor_name',
            'port',
            'dim_location', 'dim_location_read_only', # Write and read only fields
            'is_active', 'is_active_read_only', # Write and read only fields
            # 'is_placeholder', 'is_placeholder_read_only', # Write and read only fields
            # 'placeholder_level',
        )


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


class DimConstructionTypeSerializer(serializers.ModelSerializer):
    r"""
    Serializers for DimConstructionType
    """

    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.DimConstructionType
        fields = model.get_form_field_names_tuple(model)


class DimProductSerializer(serializers.ModelSerializer):
    r"""
    Serializers for DimProduct
    """

    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.DimProduct
        fields = model.get_form_field_names_tuple(model)


class FactCapacitySerializer(
    mixins_serializer.ProductionLineLookup,
    mixins_serializer.XFDateLookup,
    serializers.ModelSerializer
):
    r"""
    Serializers for FactCapacity
    """

    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.FactCapacity
        fields = (
            'id',
            'dim_production_line', 'dim_production_line_read_only', # Write and read only fields
            'dim_date_month_xf', 'dim_date_month_xf_read_only', # Write and read only fields
            'quantity',
        )
