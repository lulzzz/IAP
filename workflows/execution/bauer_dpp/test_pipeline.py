import sys
import os

# Navigate to Django root folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(sys.path[0]))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.projects.settings_bauer_dpp.project")
from django.conf import settings as cp

from workflows.core import os_utils
from workflows.core import df_utils
from workflows.extractions.standards.core import pipeline


filename_dict = os_utils.get_file_properties(
    folder=cp.INPUT_DIRECTORY,
    result_format='file_property_dict',
    # startswith='PDAS',
    extension_list=['xlsx'],
)

# Load extracts
pipeline.s01_load_extracts(filename_dict, reload=True)
