import sys
import os

# Navigate to Django root folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(sys.path[0]))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.projects.settings_tattoo.project")
from django.conf import settings as cp

from workflows.extractions.projects.tattoo import tattoodo_crawler

tattoodo_crawler.exploit_api(
    api_url='https://backend-api.tattoodo.com/api/v2/search/posts',
    max_page=1000,
    limit=24,
    output_directory=cp.OUTPUT_DIRECTORY,
)
