import pandas as pd
from decimal import *

def upsert_featurestoreinput(session, dbo):

    query = session.query(dbo.app_dms_dimproduct)
    products = pd.read_sql(query.statement, query.session.bind)

    query = session.query(dbo.app_dms_dimstore)
    stores = pd.read_sql(query.statement, query.session.bind)

    # Query all entries already existing
    existing_objects = session.query(dbo.app_dms_featurestoreinput).all()
    existing = {(o.dim_store_id, o.dim_iapfilter_id):o for o in existing_objects}

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

        group_mean = movements.groupby('dim_store_id').mean().reset_index()

        group_sum = movements.groupby('dim_store_id').sum().reset_index()

        sku_count = movements.groupby(['dim_store_id', 'dim_product_id']).count(
        ).groupby('dim_store_id').count()['units'].reset_index()

        swimwear = movements[movements['division'] == '103 SWIMWEAR'].groupby('dim_store_id').sum().reset_index()
        lingerie = movements[movements['division'] == '104 LINGERIE'].groupby('dim_store_id').sum().reset_index()
        legwear = movements[movements['division'] == '101 LEGWEAR'].groupby('dim_store_id').sum().reset_index()
        ready = movements[movements['division'] == '102 READY-TO-WEAR'].groupby('dim_store_id').sum().reset_index()
        adv = movements[movements['division'] == '190 ADV.+PROMOTION'].groupby('dim_store_id').sum().reset_index()
        accessories = movements[movements['division'] == '180 ACCESSORIES'].groupby('dim_store_id').sum().reset_index()

        # Build entries based on existing ones

        for store_id in movements['dim_store_id'].unique():
            record = existing.get((store_id, iapfilter.id))

            # Create default entry
            entry = dict()

            entry['dim_iapfilter_id'] = iapfilter.id
            entry['dim_store_id'] = store_id
            entry['net_retail_sales_in_eur_ty'] = group_sum[group_sum['dim_store_id'] == store_id]['salesvalue'].iloc[0]
            entry['average_monthly_sales_for_ty'] = entry['net_retail_sales_in_eur_ty'] / 6
            entry['sku_count'] = sku_count[sku_count['dim_store_id'] == store_id]['units'].iloc[0]
    #         entry['relative_sales_volume_ty'] = group_sum[group_sum['dim_store_id'] == store_id]['units'].iloc[0]
            entry['average_value_transaction'] = group_mean[group_mean['dim_store_id'] == store_id]['salesvalue'].iloc[0]
            if store_id in swimwear['dim_store_id'].values:
                entry['sales_swimwear'] = swimwear[swimwear['dim_store_id'] == store_id]['salesvalue'].iloc[0]
            else:
                entry['sales_swimwear'] = 0.
            if store_id in lingerie['dim_store_id'].values:
                entry['sales_lingerie'] = lingerie[lingerie['dim_store_id'] == store_id]['salesvalue'].iloc[0]
            else:
                entry['sales_lingerie'] = 0.
            if store_id in legwear['dim_store_id'].values:
                entry['sales_legwear'] = legwear[legwear['dim_store_id'] == store_id]['salesvalue'].iloc[0]
            else:
                entry['sales_legwear'] = 0.
            if store_id in ready['dim_store_id'].values:
                entry['sales_ready_to_wear'] = ready[ready['dim_store_id'] == store_id]['salesvalue'].iloc[0]
            else:
                entry['sales_ready_to_wear'] = 0.
            if store_id in adv['dim_store_id'].values:
                entry['sales_adv_promotion'] = adv[adv['dim_store_id'] == store_id]['salesvalue'].iloc[0]
            else:
                entry['sales_adv_promotion'] = 0.
            if store_id in accessories['dim_store_id'].values:
                entry['sales_accessories'] = accessories[accessories['dim_store_id'] == store_id]['salesvalue'].iloc[0]
            else:
                entry['sales_accessories'] = 0.
            entry['cluster_ai'] = 'XX'
            entry['cluster_user'] = 'XX'
            entry['optimal_assortment_similarity_coefficient'] = 0

            # Convert floats to int
            for k,v in entry.items():
                if k in ('dim_store_id', 'sku_count', 'dim_iapfilter_id'):
                    entry[k] = int(round(v,0))
                elif k not in ('optimal_assortment_similarity_coefficient', 'cluster_ai', 'cluster_user'):
                    entry[k] = Decimal(v)

            if record is not None:
                # Update record
                update_count += 1

                for k,v in entry.items():
                    if k != 'cluster_user':
                        setattr(record, k, v)

            else:
                insert_count += 1
                to_insert.append(dbo.app_dms_featurestoreinput(**entry))

        session.commit()
        total_update += update_count
        total_insert += insert_count
        print('Updated:', update_count, '| To Insert:', insert_count)

    # Only add those posts which did not exist in the database
    session.bulk_save_objects(to_insert)

    # Now we commit our modifications (merges) and inserts (adds) to the database!
    session.commit()

    print('Total Updated:', total_update, 'Total Inserted:', total_insert)
