import sys
import os

# Navigate to Django root folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(sys.path[0]))))

from manage import PROJECT_SETTINGS
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.projects.settings_wolford_iap.project")
from django.conf import settings as cp

from workflows.transformations.projects.wolford_iap import consolidated_plan


def generate_consolidated_plan():
    r"""
    Generate the consolidated plan
    """
    # Generate plan
    consolidated_plan.run()

    # Export to Excel

    
    return True
