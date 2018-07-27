from sqlalchemy.orm import aliased
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine, and_
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func, text
from sqlalchemy.ext.automap import automap_base
import pandas as pd

from workflows.core.database_utils import db_connect

# Create connection to database, TODO: these needs to be put somehwere else
engine = db_connect()
Session = sessionmaker(bind=engine)

Base = automap_base()
Base.prepare(engine, reflect=True)

dbo = Base.classes
session = Session()

def run(dim_iapfilter):

    # Query data from database
    planbymonths = session.query(dbo.app_dms_planbymonth).filter(dbo.app_dms_planbymonth.dim_iapfilter_id == dim_iapfilter).all()
    planbystores = session.query(dbo.app_dms_planbystore).filter(dbo.app_dms_planbystore.dim_iapfilter_id == dim_iapfilter).all()
    dim_store = session.query(dbo.app_dms_dimstore).all()
    dim_store_ids_by_code = {store.store_code:store.id for store in dim_store}
    categories = session.query(dbo.app_dms_planbyproductcategory).filter(dbo.app_dms_planbyproductcategory.dim_iapfilter_id == dim_iapfilter).all()

    # Delete existing entries
    items = session.query(
        dbo.app_dms_planbymonthproductcategorystore
    ).filter(
        dbo.app_dms_planbymonthproductcategorystore.dim_iapfilter_id == dim_iapfilter
    ).all()
    for item in items:
        session.delete(item)

    session.commit()

    # Compute totals
    total_unit_sales_py_store = sum([planbystore.unit_sales_py for planbystore in planbystores])
    total_value_sales_py_store = sum([planbystore.value_sales_py for planbystore in planbystores])
    total_unit_sales_py_category = sum([category.unit_sales_py for category in categories])
    total_value_sales_py_category = sum([category.value_sales_py for category in categories])

    # Create entries and store into a temporary list
    objects = list()
    for planbymonth in planbymonths:
        for planbystore in planbystores:
            for category in categories:
                unit_sales_py = planbymonth.unit_sales_py_year_month_level \
                                * planbystore.unit_sales_py / total_unit_sales_py_store \
                                * category.unit_sales_py / total_unit_sales_py_category

                value_sales_py = planbymonth.value_sales_py_year_month_level \
                                * planbystore.value_sales_py / total_value_sales_py_store \
                                * category.value_sales_py / total_value_sales_py_category

                objects.append(
                    dbo.app_dms_planbymonthproductcategorystore(
                        dim_iapfilter_id = planbymonth.dim_iapfilter_id,
                        year_month_name_ly = planbymonth.year_month_name_ly,
                        year_month_name_py = planbymonth.year_month_name_py,
                        dim_store_id = dim_store_ids_by_code.get(planbystore.store_code, 0),
                        cluster_user = planbystore.cluster_user,
                        product_category = category.product_category,
                        product_division = category.product_division,
                        unit_sales_py = unit_sales_py,
                        value_sales_py = value_sales_py,
                    )
                )

    # Save entries from temporary list to database
    session.bulk_save_objects(objects)


def export_to_excel(dim_iapfilter, output_path):
    # Variables
    sheetname = 'IAP Export'

    # Query data
    export_data = session.query(
        dbo.app_dms_planbymonthproductcategorystore, dbo.app_dms_dimstore, dbo.app_dms_dimlocation
    ).filter(
        dbo.app_dms_planbymonthproductcategorystore.dim_store_id == dbo.app_dms_dimstore.id,
        dbo.app_dms_dimlocation.id == dbo.app_dms_dimstore.dim_location_id,
        dbo.app_dms_planbymonthproductcategorystore.dim_iapfilter_id == dim_iapfilter
    ).all()

    # Transform data into pandas Data Frame
    entries = list()
    for categorystore, dimstore, dimlocation in export_data:
        entries.append({
            'month PY' : categorystore.year_month_name_py,
            'cluster' : categorystore.cluster_user,
            'product category' : categorystore.product_category,
            'product division' : categorystore.product_division,
            'unit sales' : categorystore.unit_sales_py,
            'value sales' : round(categorystore.value_sales_py, 2),
            'store name' : dimstore.store_name,
            'store country' : dimlocation.country
        })

    df_export = pd.DataFrame(entries)

    # Reorder columns
    df_export = df_export[['month PY', 'cluster', 'product category', 'product division', 'unit sales', 'value sales', 'store name', 'store country']]

    # Filter out where unit sales != 0
    df_export = df_export[df_export['unit sales'] != 0]

    # Export to excel
    writer = pd.ExcelWriter(output_path)
    df_export.to_excel(writer, sheetname, index = False)
    writer.save()
