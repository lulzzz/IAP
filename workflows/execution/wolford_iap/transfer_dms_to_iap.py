import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(sys.path[0]))))

# Update insert into dim product
from workflows.remote_procedure.wolford_iap import calls_dms

# Generate dim_product
productattributetypeid_dict = {
    'Colour': '2',
    'ProductType': '5',
    'Season': '6',
    'Size': '7',
    'Style': '8',
    'Category': '9',
    'Division': '12',
    'Quality': '18',
    'Essential Trend': '19',
    'Basic Fashion Colour': '20',
}

# Update insert into dim product
# calls_dms.upsert_dim_product(productattributetypeid_dict)

# Update insert into dim store
# calls_dms.upsert_dim_store()

# Load new fact movement entries
calls_dms.load_new_fact_movements()
