import sys
import os

# Navigate to Django root folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(sys.path[0]))))

from manage import PROJECT_SETTINGS
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.projects.settings_bauer_dpp.project")
from django.conf import settings as cp

from workflows.extractions.projects.bauer_dpp import etl_processes
from workflows.transformations.projects.bauer_dpp import unconstrained_allocation


def launch_extraction_etl():
    r"""
    Extract files from ETL folder
    """
    source_file_path = cp.SOURCE_FOLDER_ETL
    etl_processes.get_data_from_extracts(source_file_path)
    return True


def launch_allocation():
    r"""
    Run decision tree algorithm (all scenarios)
    """
    allocation.run()
    return True
