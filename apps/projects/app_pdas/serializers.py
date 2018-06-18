from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from . import models
from . import mixins_serializer
from core import utils


class DimReleaseSerializer(
    mixins_serializer.DemandCategoryLookup,
    mixins_serializer.BuyingProgramFullLookup,
    serializers.ModelSerializer
):
    r"""
    Serializer for master table
    """

    # Read-only fields
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.DimRelease
        fields = (
            'id',
            'dim_demand_category', 'dim_demand_category_read_only', # Write and read only fields
            'dim_buying_program', 'dim_buying_program_read_only', # Write and read only fields
            'buy_month',
            'dim_date',
            'comment',
        )

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


class DimFactorySerializer(
    mixins_serializer.DimLocationLookup,
    mixins_serializer.IsActiveLookup,
    mixins_serializer.IsPlaceholderLookup,
    serializers.ModelSerializer
):

    # Read-only fields
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.DimFactory
        fields = (
            'id',
            'dim_location', 'dim_location_read_only', # Write and read only fields
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
            'is_active', 'is_active_read_only', # Write and read only fields
            'is_placeholder', 'is_placeholder_read_only', # Write and read only fields
            'placeholder_level',
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


class HelperPdasFootwearVansAvgFobSerializer(
    mixins_serializer.FactoryShortNameLookup,
    mixins_serializer.MaterialIDLookup,
    serializers.ModelSerializer
):
    r"""
    Serializer for master table
    """

    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.HelperPdasFootwearVansAvgFob
        fields = model.get_form_field_names_tuple(model)


class HelperPdasFootwearVansCutoffSerializer(
    mixins_serializer.CountryCodeA2Lookup,
    serializers.ModelSerializer
):
    r"""
    Serializer for master table
    """

    id = serializers.IntegerField(read_only=True)
    port_code = serializers.CharField(min_length=2)
    port_name = serializers.CharField(min_length=2)

    class Meta:
        model = models.HelperPdasFootwearVansCutoff
        fields = model.get_form_field_names_tuple(model)

    # Validation rules
    def validate_cutoff_day_eu_dc(self, value):
        value = value.replace(' ', '').title()
        valid_values = utils.get_weekday_list()
        if value in valid_values:
            return value
        raise serializers.ValidationError('Value must be one of the following: ' + ', '.join(map(str, valid_values)))

    def validate_cutoff_day_eu_crossdock(self, value):
        value = value.replace(' ', '').title()
        valid_values = utils.get_weekday_list()
        if value in valid_values:
            return value
        raise serializers.ValidationError('Value must be one of the following: ' + ', '.join(map(str, valid_values)))


class HelperPdasFootwearVansFactoryCapacityAdjustmentSerializer(
    mixins_serializer.FactoryShortNameLookup,
    serializers.ModelSerializer
):
    r"""
    Serializer for master table
    """

    id = serializers.IntegerField(read_only=True)
    # percentage_read_only = serializers.SerializerMethodField()
    # percentage_adjustment_read_only = serializers.SerializerMethodField()
    #
    # # Read-only methods (get_ is a DRF prefix)
    # def get_percentage_read_only(self, model):
    #     return utils.convert_float_to_percentage(model.percentage)
    #
    # def get_percentage_adjustment_read_only(self, model):
    #     return utils.convert_float_to_percentage(model.percentage_adjustment)
    #
    # # Write-only fields
    # percentage = serializers.FloatField(write_only=True)
    # percentage_adjustment = serializers.FloatField(write_only=True)

    class Meta:
        model = models.HelperPdasFootwearVansFactoryCapacityAdjustment
        fields = model.get_form_field_names_tuple(model)
        # fields = (
        #     'id',
        #     'factory_short_name',
        #     'percentage', 'percentage_read_only', # Write and read only fields
        #     'percentage_adjustment', 'percentage_adjustment_read_only', # Write and read only fields
        # )

    # Validation rules
    def validate_percentage(self, value):
        # value = utils.percentage_to_float(value)
        if value <= 1:
            return value
        raise serializers.ValidationError('Must be a valid decimal less or equal to 1')

    def validate_percentage_adjustment(self, value):
        # value = utils.percentage_to_float(value)
        if value <= 1:
            return value
        raise serializers.ValidationError('Must be a valid decimal less or equal to 1')


class HelperPdasFootwearVansFactoryCapacityByRegionSerializer(
    mixins_serializer.FactoryShortNameLookup,
    serializers.ModelSerializer
):
    r"""
    Serializer for master table
    """

    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.HelperPdasFootwearVansFactoryCapacityByRegion
        fields = model.get_form_field_names_tuple(model)

    # Validation rules
    max_value = 1
    def validate(self, data):
        if (data['emea'] + data['apac'] + data['casa'] + data['nora'] != self.max_value):
            raise serializers.ValidationError('Sum of regions must be exactly ' + str(self.max_value))
        return data

    def validate_emea(self, value):
        if value <= self.max_value:
            return value
        raise serializers.ValidationError('Must be a valid decimal less or equal to ' + str(self.max_value))

    def validate_casa(self, value):
        if value <= self.max_value:
            return value
        raise serializers.ValidationError('Must be a valid decimal less or equal to ' + str(self.max_value))

    def validate_nora(self, value):
        if value <= self.max_value:
            return value
        raise serializers.ValidationError('Must be a valid decimal less or equal to ' + str(self.max_value))

    def validate_apac(self, value):
        if value <= self.max_value:
            return value
        raise serializers.ValidationError('Must be a valid decimal less or equal to ' + str(self.max_value))



class HelperPdasFootwearVansFtyQtSerializer(
    mixins_serializer.FactoryShortNameLookup,
    mixins_serializer.MaterialIDLookup,
    serializers.ModelSerializer
):
    r"""
    Serializer for master table
    """

    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.HelperPdasFootwearVansFtyQt
        fields = model.get_form_field_names_tuple(model)



class HelperPdasFootwearVansLabelUpchargeSerializer(
    mixins_serializer.ProductTypeLookup,
    mixins_serializer.CustomerNameLookup,
    serializers.ModelSerializer
):
    r"""
    Serializer for master table
    """

    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.HelperPdasFootwearVansLabelUpcharge
        fields = model.get_form_field_names_tuple(model)

    # Validation rules
    product_type_list = ['Shoes', 'Sandal', 'All']


class HelperPdasFootwearVansMappingSerializer(serializers.ModelSerializer):
    r"""
    Serializer for master table
    """

    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.HelperPdasFootwearVansMapping
        fields = model.get_form_field_names_tuple(model)

    # Validation rules
    def validate(self, data):
        if (data['category'] == 'Factory Master' and not
            models.DimFactory.objects.filter(short_name=data['parent']).exists()
        ):
            raise serializers.ValidationError('Value must exist in factory master')

        if (data['category'] == 'Customer Master' and not
            models.DimCustomer.objects.filter(name=data['parent']).exists()
        ):
            raise serializers.ValidationError('Value must exist in customer master')

        if (data['category'] == 'Construction Type Master' and not
            models.DimConstructionType.objects.filter(name=data['parent']).exists()
        ):
            raise serializers.ValidationError('Value must exist in construction type master')

        return data

    def validate_category(self, value):
        value = value.title()
        valid_values = [
            'Factory Master',
            'Customer Master',
            'Construction Type Master'
        ]
        if value in valid_values:
            return value
        raise serializers.ValidationError('Value must be one of the following: ' + ', '.join(map(str, valid_values)))


class HelperPdasFootwearVansMoqPolicySerializer(
    mixins_serializer.ProductTypeLookup,
    serializers.ModelSerializer
):
    r"""
    Serializer for master table
    """

    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.HelperPdasFootwearVansMoqPolicy
        fields = model.get_form_field_names_tuple(model)

    # Validation rules
    product_type_list  = ['Regular', 'Vault']


class HelperPdasFootwearVansPrebuildSerializer(
    mixins_serializer.FactoryShortNameLookup,
    mixins_serializer.MaterialIDLookup,
    mixins_serializer.BuyingProgramLookup,
    mixins_serializer.RegionLookup,
    serializers.ModelSerializer
):
    r"""
    Serializer for master table
    """

    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.HelperPdasFootwearVansPrebuild
        fields = model.get_form_field_names_tuple(model)


class HelperPdasFootwearVansRetailQtSerializer(
    mixins_serializer.FactoryShortNameLookup,
    mixins_serializer.MaterialIDLookup,
    mixins_serializer.BuyingProgramLookup,
    mixins_serializer.RegionLookup,
    mixins_serializer.SoldToPartyLookup,
    serializers.ModelSerializer
):
    r"""
    Serializer for master table
    """

    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.HelperPdasFootwearVansRetailQt
        fields = model.get_form_field_names_tuple(model)



class HelperPdasFootwearVansPerformanceSerializer(
    serializers.ModelSerializer
):
    r"""
    Serializer for master table
    """

    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.HelperPdasFootwearVansPerformance
        fields = model.get_form_field_names_tuple(model)
