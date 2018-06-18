from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from . import models

class HelperPdasFootwearVansReleaseCurrentForm(forms.ModelForm):
    r"""
    Form for HelperPdasFootwearVansReleaseCurrent model
    """

    class Meta:
        model = models.HelperPdasFootwearVansReleaseCurrent
        fields = (
            'dim_release',
        )


class ProductForm(forms.ModelForm):
    r"""
    Form for model
    """
    # dim_vendor = forms.ModelChoiceField(queryset=models.DimVendor.objects.all(), label='Vendor')

    class Meta:
        model = models.DimProduct
        exclude = ('dim_business', 'is_placeholder', 'placeholder_level',)


class VendorForm(forms.ModelForm):
    r"""
    Form for model
    """
    dim_location = forms.ModelChoiceField(queryset=models.DimLocation.objects.all(), label='COO')

    class Meta:
        model = models.DimFactory
        exclude = ('dim_business', 'is_placeholder', 'placeholder_level',)
