from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from . import models

class ProductForm(forms.ModelForm):
    r"""
    Form for DimProduct model
    """

    class Meta:
        model = models.DimProduct
        fields = (
            'division',
            'category',
            'productdescription',
            'style',
            'colour',
            'size',
            'essential_trend',
            'basic_fashion',
            'quality',
        )


class StoreForm(forms.ModelForm):
    r"""
    Form for DimStore model
    """

    class Meta:
        model = models.DimStore
        fields = (
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
            'store_style',
            'customer_type',
            'potential',
            'store_size',
            'store_tier',
            'is_active',
        )
