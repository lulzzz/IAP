import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(sys.path[0]))))

from sqlalchemy.ext.automap import automap_base

from workflows.execution.wolford_iap import Session, engine
from workflows.transformations.projects.wolford_iap.upsert_featurestoreinput import upsert_featurestoreinput
from workflows.transformations.projects.wolford_iap.upsert_featurestoreinput_cluster import upsert_featurestoreinput_cluster

# Creating database session
session = Session()

# Generate mapped classes and relationships from database reflected schema
Base = automap_base()
Base.prepare(engine, reflect=True)

dbo = Base.classes

upsert_featurestoreinput(session, dbo)

# Example
user_input = {
    'store_fields':[
        'store_size',
        'store_style',
        'store_tier',
#         'customer_type',
        'net_retail_sales_in_eur_ty',
        'region',
        'country',
#         'potential',
        'sku_count',
        'sales_lingerie',
        'sales_legwear',
        'sales_ready_to_wear',
        'sales_accessories',
        'sales_adv_promotion'
    ],
    'cluster_number': 6
}

upsert_featurestoreinput_cluster(session, dbo, user_input)
