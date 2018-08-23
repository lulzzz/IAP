import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(sys.path[0]))))

from sqlalchemy.ext.automap import automap_base

from workflows.execution.wolford_iap import Session, engine
from workflows.transformations.projects.wolford_iap.upsert_strategicplan import upsert_strategicplan

# Creating database session
session = Session()

# Generate mapped classes and relationships from database reflected schema
Base = automap_base()
Base.prepare(engine, reflect=True)

dbo = Base.classes

upsert_strategicplan(session, dbo)
