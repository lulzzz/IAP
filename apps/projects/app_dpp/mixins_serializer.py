from rest_framework import serializers

from . import models

class DimLocationLookup(serializers.Serializer):
    r"""
    Validation mixin that does a lookup for finding country code A2 for dim_location_id
    """

    # Read-only field
    dim_location_read_only = serializers.SerializerMethodField()

    # Write-only fields
    dim_location = serializers.CharField(write_only=True)

    # Read-only methods (get_ is a DRF prefix)
    def get_dim_location_read_only(self, obj):
        return obj.dim_location.country_code_a2

    # Validation rules
    def validate_dim_location(self, value):
        model_item = models.DimLocation.objects.filter(country_code_a2=value)
        if model_item.count() > 0:
            return model_item.first()
        raise serializers.ValidationError('Value must exist in location master')


class DimFactoryLookup(serializers.Serializer):
    r"""
    Validation mixin that does a lookup for finding factory plant code
    """

    # Read-only field
    dim_factory_read_only = serializers.SerializerMethodField()

    # Write-only fields
    dim_factory = serializers.CharField(write_only=True)

    # Read-only methods (get_ is a DRF prefix)
    def get_dim_factory_read_only(self, obj):
        return obj.dim_factory.plant_code

    # Validation rules
    def validate_dim_factory(self, value):
        model_item = models.DimFactory.objects.filter(plant_code=value)
        if model_item.count() > 0:
            return model_item.first()
        raise serializers.ValidationError('Value must exist in factory master')


class IsActiveLookup(serializers.Serializer):
    r"""
    Validation mixin that does the boolean field conversion
    """

    # Read-only field
    is_active_read_only = serializers.SerializerMethodField()

    # Write-only fields
    is_active = serializers.CharField(write_only=True)

    # Read-only methods (get_ is a DRF prefix)
    def get_is_active_read_only(self, obj):
        return 'Y' if obj.is_active else 'N'

    # Validation rules
    def validate_is_active(self, value):
        value = value[:1].upper()
        valid_values = ['Y', 'N']
        if value in valid_values:
            return True if value == 'Y' else False
        raise serializers.ValidationError('Value must be one of the following: ' + ', '.join(map(str, valid_values)))


class IsPlaceholderLookup(serializers.Serializer):
    r"""
    Validation mixin that does the boolean field conversion
    """

    # Read-only field
    is_placeholder_read_only = serializers.SerializerMethodField()

    # Write-only fields
    is_placeholder = serializers.CharField(write_only=True)

    # Read-only methods (get_ is a DRF prefix)
    def get_is_placeholder_read_only(self, obj):
        return 'Y' if obj.is_placeholder else 'N'

    # Validation rules
    def validate_is_placeholder(self, value):
        value = value[:1].upper()
        valid_values = ['Y', 'N']
        if value in valid_values:
            return True if value == 'Y' else False
        raise serializers.ValidationError('Value must be one of the following: ' + ', '.join(map(str, valid_values)))


class RegionLookup(serializers.Serializer):
    r"""
    Validation mixin that checks the region value
    """

    # Validation rules
    def validate_region(self, value):
        value = value.upper()
        valid_values = ['APAC', 'NORA', 'EMEA', 'CASA']
        if value in valid_values:
            return value
        raise serializers.ValidationError('Value must be one of the following: ' + ', '.join(map(str, valid_values)))


class FactoryCodeLookup(serializers.Serializer):
    r"""
    Validation mixin that checks the factory short name
    """

    # Validation rules
    def validate_factory_short_name(self, value):
        if models.DimFactory.objects.filter(plant_code=value).exists():
            return value
        raise serializers.ValidationError('Value must exist in factory master')


class ProductionLineLookup(serializers.Serializer):
    r"""
    Validation mixin that checks the production line
    """

    # Read-only field
    dim_production_line_read_only = serializers.SerializerMethodField()

    # Write-only fields
    dim_production_line = serializers.CharField(write_only=True)

    # Read-only methods (get_ is a DRF prefix)
    def get_dim_production_line_read_only(self, obj):
        return obj.dim_production_line.line

    # Validation rules
    def validate_dim_production_line(self, value):
        model_item = models.DimProductionLine.objects.filter(line=value)
        if model_item.count() > 0:
            return model_item.first()
        raise serializers.ValidationError('Value must exist in production line master')


class XFDateLookup(serializers.Serializer):
    r"""
    Validation mixin that checks the date
    """

    # Read-only field
    dim_date_month_xf_read_only = serializers.SerializerMethodField()

    # Write-only fields
    dim_date_month_xf = serializers.CharField(write_only=True)

    # Read-only methods (get_ is a DRF prefix)
    def get_dim_date_month_xf_read_only(self, obj):
        return obj.dim_date_month_xf.year_month

    # Validation rules
    def validate_dim_date_month_xf(self, value):
        model_item = models.DimDate.objects.filter(year_month=value).order_by('id')
        if model_item.count() > 0:
            return model_item.first()
        raise serializers.ValidationError('Value must be a valid date')


class SKULookup(serializers.Serializer):
    r"""
    Validation mixin that checks the material ID
    """

    # Validation rules
    def validate_mtl(self, value):
        return value
        if models.DimProduct.objects.filter(sku=value).exists():
            return value
        raise serializers.ValidationError('Value must exist in product master')


class CountryCodeA2Lookup(serializers.Serializer):
    r"""
    Validation mixin that checks the country code A2
    """

    # Validation rules
    def validate_country_code_a2(self, value):
        if models.DimLocation.objects.filter(country_code_a2=value).exists():
            return value
        raise serializers.ValidationError('Value must exist in location master')


class CustomerNameLookup(serializers.Serializer):
    r"""
    Validation mixin that checks the customer name
    """

    # Validation rules
    def validate_customer_name(self, value):
        if models.DimCustomer.objects.filter(name=value).exists():
            return value
        raise serializers.ValidationError('Value must exist in customer master')


class ProductTypeLookup(serializers.Serializer):
    r"""
    Validation mixin that checks the product type based on a given product_type_list
    """

    # Validation rules
    def validate_product_type(self, value):
        value = value.title()
        valid_values = self.product_type_list
        if value in valid_values:
            return value
        raise serializers.ValidationError('Value must be one of the following: ' + ', '.join(map(str, valid_values)))
