import sys
import os
# Navigate to Django root folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(sys.path[0]))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.projects.settings_vans_pdas.project")
from django.conf import settings

# Update insert into dim product
from workflows.execution.vans_pdas import calls


calls.launch_unconstrained_allocation()
