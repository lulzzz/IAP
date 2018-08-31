import pandas as pd
from decimal import *

def upsert_featurestoreinput(session, dbo):

    query = session.query(dbo.app_dms_dimproduct)
    products = pd.read_sql(query.statement, query.session.bind)

    query = session.query(dbo.app_dms_dimstore)
    stores = pd.read_sql(query.statement, query.session.bind)

    # Query all entries already existing
    existing_objects = session.query(dbo.app_dms_featureproductinput).all()
    existing = {(o.dim_store_id, o.dim_product_id, o.dim_iapfilter_id):o for o in existing_objects}

    # We loop by dimaipfilter to avoid querring fact movements all at once
    dimaipfilter = session.query(dbo.app_dms_dimiapfilter).all()

    # List of entries to insert intod database
    to_insert = list()
    total_update = 0
    total_insert = 0

    for iapfilter in dimaipfilter:

        # Dates associated to this iap filter
        iap_dimdate = session.query(
            dbo.app_dms_dimdate.id
        ).filter(
            dbo.app_dms_dimdate.sales_year == iapfilter.sales_year,
            dbo.app_dms_dimdate.sales_season == iapfilter.sales_season,
        ).all()

        dates = [d[0] for d in iap_dimdate]

        # Get movements
        query = session.query(
            dbo.app_dms_factmovements.units,
            dbo.app_dms_factmovements.salesvalue,
            dbo.app_dms_factmovements.dim_product_id,
            dbo.app_dms_factmovements.dim_store_id,
        ).filter(
            dbo.app_dms_factmovements.dim_date_id.in_(dates)
        )

        movements_raw = 0
        movements_raw = pd.read_sql(query.statement, query.session.bind)

        # Join with stores and filter with only iapfilter.dim_channel_id
        movements = 0
        movements = movements_raw.merge(stores, how='left', left_on='dim_store_id', right_on='id')
        movements = movements[movements['dim_channel_id'] == iapfilter.dim_channel_id]

        print(iapfilter.sales_year, iapfilter.sales_season, iapfilter.dim_channel_id, movements_raw.shape, '->', movements.shape)
        update_count = 0
        insert_count = 0

        # Join with products and aggregate
        movements = movements.merge(products, how='left', left_on='dim_product_id', right_on='id')

        group_sum = movements.groupby(['dim_store_id', 'dim_product_id']).sum().reset_index()

        # Build entries based on existing ones

        for idx, row in group_sum.iterrows():
            record = existing.get((row.dim_store_id, row.dim_product_id, iapfilter.id))

            # Create default entry
            entry = dict()

            # Input values in constant fields
            entry['units'] = row.units
            entry['salesvalueeur'] = row.salesvalue
            entry['cluster_ai'] = 'XX'
            entry['cluster_user'] = 'XX'
            entry['dim_iapfilter_id'] = iapfilter.id
            entry['dim_product_id'] = row.dim_product_id
            entry['dim_store_id'] = row.dim_store_id

            # Convert floats to int
            for k,v in entry.items():
                if k in ('dim_store_id', 'units', 'dim_iapfilter_id', 'dim_product_id'):
                    entry[k] = int(v)
                elif k not in ('cluster_ai', 'cluster_user'):
                    entry[k] = Decimal(v)

            if record is not None:
                # Update record
                update_count += 1

                for k,v in entry.items():
                    if k != 'cluster_user':
                        setattr(record, k, v)

            else:
                insert_count += 1
                to_insert.append(dbo.app_dms_featureproductinput(**entry))

        session.commit()
        total_update += update_count
        total_insert += insert_count
        print('Updated:', update_count, '| To Insert:', insert_count)

    # Only add those posts which did not exist in the database
    session.bulk_save_objects(to_insert)

    # Now we commit our modifications (merges) and inserts (adds) to the database!
    session.commit()

    print('Total Updated:', total_update, 'Total Inserted:', total_insert)
