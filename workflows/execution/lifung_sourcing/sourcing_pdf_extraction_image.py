import sys
import os
import time
import pandas as pd
from tabula import read_pdf
from tqdm import tqdm

# Navigate to Django root folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(sys.path[0]))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.projects.settings_lifung_sourcing.project")
from django.conf import settings

from workflows.generic.os_utils import get_file_properties
from workflows.generic.database_utils import load_to_staging_area
from workflows.pdf.table_extractor import read_all_pdf, extract_measurement_table, extract_top_table
from workflows.pdf.image_extractor import extract_images_from_pdf
from workflows.execution.lifung_sourcing import Session, engine
from sqlalchemy.ext.automap import automap_base

# Start time
start_time = time.time()

# Creating database session
session = Session()

# Generate mapped classes and relationships from database reflected schema
Base = automap_base()
Base.prepare(engine, reflect=True)

# Variable definition and file focus
ignore_meta = False
input_folder = settings.INPUT_DIRECTORY
output_folder = settings.OUTPUT_DIRECTORY

# Get file names to process
file_properties = get_file_properties(input_folder)
file_properties_filtered = []
for file_property in file_properties:
    # if file_property['name'].lower().startswith('a') and file_property['extension'] == '.pdf':
    if file_property['extension'] == '.pdf':
        file_properties_filtered.append(file_property)


r"""
Extract images from PDF files
"""
print()
print('Start image extraction')
start_time = time.time()

print(len(file_properties_filtered), 'PDF files selected')
result_list = list()
for file_property in file_properties_filtered:
    database_atoms = extract_images_from_pdf(
        file_property,
        output_folder,
        page_limit=1,
        image_on_page_limit=5
    )

    # if database_atoms and len(database_atoms) > 0:
    #     load_to_staging_area(session, Base, database_atoms, ignore_meta=ignore_meta)

# print(result_list)
success_count = 0
invalid_pdf_list = list()


print('-' * 100)
print('Summary')
if len(result_list) > 0:
    print(str(sum(result_list)) + '/' + str(len(result_list)), '(' + '{0:.0f}%'.format(sum(result_list)/len(result_list) * 100) + ')', 'of images extracted successfully')
print('Duration:', '%s seconds' % int((time.time() - start_time)))
