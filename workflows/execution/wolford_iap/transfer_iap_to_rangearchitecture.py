import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(sys.path[0]))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.projects.settings_wolford_iap.project")

import django
django.setup()

from django.conf import settings
from apps.projects.app_dms import models

from workflows.remote_procedure.wolford_iap.calls_range_planning
