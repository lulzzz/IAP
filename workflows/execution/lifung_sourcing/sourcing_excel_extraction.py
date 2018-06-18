


from flat_file.source_extractor import workflow_execution

c = WorkflowControl('Gym XTS Extract (Shipped 2016 & 2017).xlsx')
c.transformation =  {
    'function': 'field_selection()',
    'kwargs': [
        'Product Attribute- Product Type Desc',
        'Product Category Desc',
        'Item Product Category Group',
    ]
}
