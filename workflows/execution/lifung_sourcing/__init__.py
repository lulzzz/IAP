import sys
import os
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(sys.path[0]))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.projects.settings_lifung_sourcing.project")

from workflows.generic.database_utils import db_connect

engine = db_connect()
Session = sessionmaker(bind=engine)
