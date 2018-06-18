from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from . import models


class HelperReleaseCurrentForm(forms.ModelForm):
    r"""
    Form for HelperReleaseCurrentForm model
    """

    class Meta:
        model = models.HelperReleaseCurrent
        fields = (
            'dim_release',
        )


class ScenarioForm(forms.ModelForm):
    r"""
    Form for model
    """
    dim_season = forms.ModelChoiceField(queryset=models.DimSeason.objects.all(), label='Season')

    class Meta:
        model = models.DimProduct
        fields = (
            'style',
        )


class ProductForm(forms.ModelForm):
    r"""
    Form for model
    """
    # dim_vendor = forms.ModelChoiceField(queryset=models.DimVendor.objects.all(), label='Vendor')

    class Meta:
        model = models.DimProduct
        exclude = ('is_placeholder', 'placeholder_level',)


class VendorForm(forms.ModelForm):
    r"""
    Form for model
    """
    dim_location = forms.ModelChoiceField(queryset=models.DimLocation.objects.all(), label='COO')

    class Meta:
        model = models.DimFactory
        exclude = ('is_placeholder', 'placeholder_level',)
