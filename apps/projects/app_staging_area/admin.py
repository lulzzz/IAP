from django.contrib import admin
from .models import SourceMaster
from .models import SourceMasterComponent
from .models import SourceMetadata
from .models import SourceMetadataFile

# SourceMaster
class SourceMasterAdmin(admin.ModelAdmin):

    list_display = ('name', 'reference')
    search_fields = ('name', 'reference')

admin.site.register(SourceMaster, SourceMasterAdmin)


#SourceMasterComponent
class SourceMasterComponentAdmin(admin.ModelAdmin):

    list_display = ('get_source_master_reference', 'category', 'label')
    search_fields = ('source_master__reference', 'category', 'label', 'reference')
    list_filter = (
        ('category', admin.AllValuesFieldListFilter),
    )

    def get_source_master_reference(self, obj):
        return obj.source_master.reference

    get_source_master_reference.short_description = 'Source Master'
    get_source_master_reference.admin_order_field = 'source_master__reference'

admin.site.register(SourceMasterComponent, SourceMasterComponentAdmin)


# SourceMetadata
class SourceMetadataAdmin(admin.ModelAdmin):

    list_display = ('get_source_master_reference', 'name', 'field_format', 'last_modified_dt', 'last_modified_by')
    list_filter = (
        ('last_modified_dt', admin.DateFieldListFilter),
    )
    search_fields = ('source_master__reference', 'category', 'label', 'reference')

    def get_source_master_reference(self, obj):
        return obj.source_master.reference

    get_source_master_reference.short_description = 'Source Master'
    get_source_master_reference.admin_order_field = 'source_master__reference'

admin.site.register(SourceMetadata, SourceMetadataAdmin)


# SourceMetadataFile
class SourceMetadataFileAdmin(admin.ModelAdmin):

    list_display = ('get_source_master_reference', 'size', 'creation_dt', 'created_by', 'relative_path')
    search_fields = ('source_metadata__source_master__reference', 'relative_path')
    list_filter = (
        ('creation_dt', admin.DateFieldListFilter),
    )

    def get_source_master_reference(self, obj):
        return obj.source_metadata.source_master.reference

    get_source_master_reference.short_description = 'Source Master'
    get_source_master_reference.admin_order_field = 'source_metadata__source_master__reference'

admin.site.register(SourceMetadataFile, SourceMetadataFileAdmin)
