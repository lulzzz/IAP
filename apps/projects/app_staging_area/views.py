from django.conf import settings as cp

from blocks import views
from core import utils
from core import mixins_view

from . import models


class MeasurementPointTable(views.TableRead):
    r"""
    View that shows the measurement points extracted from PDF file in a table
    """

    source_master_component_name = 'measurement_spec'
    source_master_component_category = 'table'
    page_length = 10

    def get_context_dict(self, request):

        # Identify the source master
        source_name = self.kwargs.get('pk', 0)

        source_master = models.SourceMaster.objects.filter(
            name=source_name
        ).first()

        # Check if table is empty
        if not source_master:
            return {
                'message': {
                    'text': 'Table does not have data',
                    'type': 'warning',
                    'position_left': True,
                }
            }

        # Master ID
        source_master_id = source_master.id

        # Page component
        source_master_component = models.SourceMasterComponent.objects.filter(
            source_master_id=source_master_id,
            category=self.source_master_component_category,
            name=self.source_master_component_name,
        )

        # Check if data available
        if source_master_component.exists():

            # Get component ID
            source_master_component_id = source_master_component.first().id

            # Table header
            header_list = list()
            data_list = list()
            format_list = list()
            source_header = models.SourceHeader
            for h in source_header.objects.filter(source_master_component=source_master_component_id):
                header_list.append(h.label)
                format_list.append(None)

                # Table data
                source_data = models.SourceData
                data_list.append(list())
                for d in source_data.objects.filter(source_header_id=h.id).order_by('row_number'):
                    data_list[len(data_list)-1].append(d.value)

            # Transpose table with data
            data_list = utils.transpose_table_horizontally(data_list)

            return {
                'header_list': header_list,
                'data_list': data_list,
                'format_list': format_list,
                'is_datatable': True,
                'page_length': self.page_length,
            }

        else:

            # Return empty table GET
            return {
                'message': {
                    'text': 'Table does not have data.',
                    'type': 'info',
                    'position_left': True,
                }
            }


class TupleTable(views.FormValidation):
    r"""
    View that shows/updates tech-pack description tuple table
    """

    template_name = 'blocks/form_validation_dict.html'
    source_master_component_category = 'tuple'

    def get_source_master_pk(self, model):
        r"""
        Get source master PK
        """
        pk = self.kwargs.get('pk', 0)
        source_master = get_object_or_404(model, pk=pk)
        source_master_id = source_master.id
        return source_master_id

    def get_context_dict(self, request):

        # Master ID
        source_master_id = self.get_source_master_pk(models.SourceMaster)

        # Page component
        source_master_component = models.SourceMasterComponent.objects.filter(
            source_master_id=source_master_id,
            category=self.source_master_component_category
        )

        form_items = list()
        if source_master_component:
            source_master_component_id = source_master_component.first().id

            # Table header
            source_header = models.SourceHeader
            for h in source_header.objects.filter(source_master_component=source_master_component_id):
                source_data = models.SourceData.objects.get(source_header_id=h.id)
                temp_dict = dict()
                temp_dict['label'] = h.label
                temp_dict['name'] = h.name
                temp_dict['value'] = source_data.value
                form_items.append(temp_dict)

        return {
            'form_items': form_items
        }
