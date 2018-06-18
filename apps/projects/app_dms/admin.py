from django.contrib import admin

from .models import DimIAPStep


# DimCustomer
class DimIAPStepAdmin(admin.ModelAdmin):

    list_display = ('name', 'position')
    # search_fields = ('name', 'code')

admin.site.register(DimIAPStep, DimIAPStepAdmin)
