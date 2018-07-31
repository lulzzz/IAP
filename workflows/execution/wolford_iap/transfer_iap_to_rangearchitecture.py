import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(sys.path[0]))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.projects.settings_wolford_iap.project")

import django
django.setup()

from django.conf import settings
from apps.projects.app_dms import models

from workflows.remote_procedure.wolford_iap.calls_range_planning

from workflows.execution.wolford_iap import Session, engine
from sqlalchemy.ext.automap import automap_base
from workflows.transformations.projects.wolford_iap.upsert_rangearchitecture import upsert_rangearchitecture

# Creating database session
session = Session()

# Generate mapped classes and relationships from database reflected schema
Base = automap_base()
Base.prepare(engine, reflect=True)

dbo = Base.classes

upsert_rangearchitecture(session, dbo)
