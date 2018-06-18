import sys
import os

# Navigate to Django root folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(sys.path[0]))))

from manage import PROJECT_SETTINGS
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.projects.settings_vans_pdas.project")
from django.conf import settings as cp

from workflows.extractions.projects.vans_pdas import etl_processes
from workflows.transformations.projects.vans_pdas import unconstrained_allocation


def launch_extraction_etl():
    r"""
    Extract files from ETL folder
    """
    source_file_path = cp.SOURCE_FOLDER_ETL
    etl_processes.get_data_from_extracts(source_file_path)
    return True


def launch_extraction_operations():
    r"""
    Extract files from Operations folder
    """
    source_file_path = cp.SOURCE_FOLDER_OPERATIONS
    etl_processes.get_data_from_extracts(source_file_path)
    return True


def launch_unconstrained_allocation():
    r"""
    Run decision tree algorithm (unconstrained)
    """
    unconstrained_allocation.run()
    return True
