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
from workflows.generic.database_utils import load_to_staging_area, pdf_exists
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
ignore_meta = True
input_folder = settings.INPUT_DIRECTORY
output_folder = settings.OUTPUT_DIRECTORY

# Get file names to process
file_properties = get_file_properties(input_folder)
file_properties_filtered = []
filename_list = list()
for file_property in file_properties:
    # if file_property['name'].lower().startswith('a') and file_property['extension'] == '.pdf':
    if file_property['extension'].lower() == '.pdf' and file_property['abs_path'].lower().find('tech') != -1:
        file_properties_filtered.append(file_property)
        filename_list.append(file_property.get('abs_path'))

r"""
Extract table content from PDF files
"""
already_added = 0
bad = list()
for file_property in tqdm(file_properties_filtered):

    if pdf_exists(file_property):
        already_added += 1
        continue

    database_atoms = extract_images_from_pdf(
        file_property,
        output_folder,
        page_limit=1,
        image_on_page_limit=1
    )

    if not database_atoms:
        bad.append(file_property)
        continue

    if database_atoms and len(database_atoms) > 0:
        load_to_staging_area(session, Base, database_atoms, ignore_meta=ignore_meta)

    table_dataframes = read_pdf(file_property['abs_path'], pages='all', multiple_tables=True, encoding='ISO-8859-1', lattice=True, silent=True)

    database_atoms = extract_top_table(file_property, table_dataframes)
    if len(database_atoms) > 0:
        load_to_staging_area(session, Base, database_atoms, ignore_meta=ignore_meta)

    database_atoms = extract_measurement_table(file_property, table_dataframes)
    if len(database_atoms) > 0:
        load_to_staging_area(session, Base, database_atoms, ignore_meta=ignore_meta)



print('-' * 100)
print('Duration:', '%s seconds' % int((time.time() - start_time)))
print('Skipped because already in database:' + already_added)
print(bad)
