from django.db import models
from django.urls import reverse


class SourceMaster(models.Model):
    name = models.CharField(max_length=500)
    label = models.CharField(max_length=500)
    reference = models.CharField(max_length=500)
    pattern = models.CharField(max_length=500)

    class Meta:
        ordering = ['reference']

    def get_absolute_url(self):
        return reverse(
            'search_tab',
            kwargs={'pk': self.pk}
        )

    def __str__(self):
        return self.reference

    @property
    def url(self):
        return self.get_absolute_url().replace('/', '#', 1)


class SourceMasterComponent(models.Model):
    source_master = models.ForeignKey(SourceMaster, models.DO_NOTHING)
    category = models.CharField(max_length=30)
    reference = models.CharField(max_length=500)
    name = models.CharField(max_length=500)
    label = models.CharField(max_length=500)

    class Meta:
        ordering = ['label']

    def __str__(self):
        return self.label

class SourceHeader(models.Model):
    source_master_component = models.ForeignKey('SourceMasterComponent', models.DO_NOTHING)
    name = models.CharField(max_length=500)
    label = models.CharField(max_length=500)
    data_type = models.CharField(max_length=30)

class SourceData(models.Model):
    source_header = models.ForeignKey('SourceHeader', models.DO_NOTHING)
    source_metadata = models.ForeignKey('SourceMetadata', models.DO_NOTHING)
    category = models.CharField(max_length=30)
    row_number = models.IntegerField()
    value = models.CharField(max_length=500, blank=True, null=True)

class SourceMetadata(models.Model):
    source_master = models.OneToOneField(SourceMaster, models.DO_NOTHING)
    name = models.CharField(max_length=500)
    field_format = models.CharField(max_length=30)
    last_modified_dt = models.DateTimeField()
    last_modified_by = models.CharField(max_length=500)

    class Meta:
        ordering = ['source_master__reference']
        verbose_name_plural = 'source metadata'

    def __str__(self):
        return self.source_master.reference

class SourceMetadataFile(models.Model):
    source_metadata = models.OneToOneField(SourceMetadata, models.DO_NOTHING, primary_key=True)
    relative_path = models.CharField(max_length=500)
    absolute_path = models.CharField(max_length=500)
    size = models.IntegerField(blank=True, null=True)
    creation_dt = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=500, blank=True, null=True)
    computer = models.CharField(max_length=500, blank=True, null=True)
    company = models.CharField(max_length=500, blank=True, null=True)
    title = models.CharField(max_length=500, blank=True, null=True)
    subject = models.CharField(max_length=500, blank=True, null=True)
    tags = models.CharField(max_length=500, blank=True, null=True)
    categories = models.CharField(max_length=500, blank=True, null=True)
    comments = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        ordering = ['source_metadata__source_master__reference']

    def __str__(self):
        return self.source_metadata.source_master.reference
