import pandas as pd
from sqlalchemy import func
from decimal import *

def upsert_strategicplan(session, dbo):

    # Query to join tables
    query = session.query(dbo.app_dms_dimproduct)
    products = pd.read_sql(query.statement, query.session.bind)

    query = session.query(dbo.app_dms_dimstore)
    stores = pd.read_sql(query.statement, query.session.bind)

    query = session.query(dbo.app_dms_dimlocation)
    location = pd.read_sql(query.statement, query.session.bind)

    query = session.query(dbo.app_dms_factinventory)
    inventory = pd.read_sql(query.statement, query.session.bind)

    # Get seasons for the loop
    latest_date = session.query(func.max(dbo.app_dms_factmovements.dim_date_id)).first()

    date = session.query(dbo.app_dms_dimdate).filter(dbo.app_dms_dimdate.id == latest_date[0]).first()

    if date.sales_season == 'SS':
        start_season = 'FW'
        start_year = date.sales_year - 1
    else:
        start_season = 'SS'
        start_year = date.sales_year

    start_dimdate_id = session.query(dbo.app_dms_dimdate.id).filter(
        dbo.app_dms_dimdate.sales_season == start_season,
        dbo.app_dms_dimdate.sales_year == start_year,
    ).first()[0]

    end_dimdate_id = start_dimdate_id + 40000

    seasons = sorted(set(session.query(
         dbo.app_dms_dimdate.sales_year, dbo.app_dms_dimdate.sales_season
    ).filter(
        dbo.app_dms_dimdate.id >= start_dimdate_id, dbo.app_dms_dimdate.id <= end_dimdate_id
    ).all()))

    seasons = seasons[:-1]


    # Query all entries already existing
    existing_objects = session.query(dbo.app_dms_strategicsalesplan).all()
    existing = {(o.sales_year, o.sales_season, o.region, o.dim_channel_id, o.scenario):o for o in existing_objects}

    # List of entries to insert intod database
    to_insert = list()
    update_count = 0

    def get_from(df, category, essential_trend, basic_fashion):
        sliced = df.loc[(df['category'] == category)
                     & (df['essential_trend'] == essential_trend)
                     & (df['basic_fashion'] == basic_fashion)]
        if sliced.shape[0] > 0:
            return int(round(sliced.iloc[0]['units'] ,0))
        return 0

    essential_basic = {'essential_trend': 'E', 'basic_fashion': 'B'}
    essential_fashion = {'essential_trend': 'E', 'basic_fashion': 'F'}
    trend_basic = {'essential_trend': 'T', 'basic_fashion': 'B'}
    trend_fashion = {'essential_trend': 'T', 'basic_fashion': 'F'}
    trends = [essential_basic, essential_fashion, trend_basic, trend_fashion]

    # Loop over (year,season)
    for season_number, season in enumerate(seasons[:2]):

        # Dates associated to the query
        iap_dimdate = session.query(
            dbo.app_dms_dimdate.id
        ).filter(
            dbo.app_dms_dimdate.sales_year == season[0],
            dbo.app_dms_dimdate.sales_season == season[1],
        ).all()

        dates = [d[0] for d in iap_dimdate]

        # Query movements
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
        movements = movements_raw.merge(stores, how='left', left_on='dim_store_id', right_on='id', suffixes=['','s_'])
    #     movements = movements[movements['dim_channel_id'] == iapfilter.dim_channel_id]
        movements = movements.merge(location, how='left', left_on='dim_location_id', right_on='id', suffixes=['','l_'])
        movements = movements.merge(products, how='left', left_on='dim_product_id', right_on='id', suffixes=['','p_'])
        movements = movements.merge(inventory, how='left', left_on=['dim_store_id', 'dim_product_id'], right_on=['storeid_id', 'productid_id'])

        # Aggregate
        movements_sum_numeric = movements.groupby(['dim_channel_id', 'region']).sum().reset_index()
        movements_sum_alpha = movements.groupby(['dim_channel_id', 'region']).first().reset_index()
        movements_sum_alpha = movements_sum_alpha[['dim_channel_id', 'region'] + list(set(movements_sum_alpha.columns) - set(movements_sum_numeric.columns))]
        movements_sum = movements_sum_alpha.merge(movements_sum_numeric, on=['dim_channel_id', 'region'])
        movements_sum.head()

        movements_inventory = movements.sort_values('inventorydate').groupby(
            ['dim_channel_id', 'region', 'dim_store_id', 'dim_product_id', 'inventorydate']
        ).sum().groupby(
            ['dim_channel_id', 'region', 'dim_store_id', 'dim_product_id']
        ).first().groupby(
            ['dim_channel_id', 'region']
        ).sum().reset_index()

        movements_sum = movements_sum.merge(movements_inventory, on=['dim_channel_id', 'region'], suffixes=['','_inventory']).fillna(0)
        # Build entries based on existing ones

        for season in seasons[season_number::2]:

            print(season[0], season[1], movements_raw.shape, '->', movements.shape)

            for i, mov in movements_sum.iterrows():

                # Create default entry
                entry = dict()

                entry['sales_year'] = season[0]
                entry['sales_season'] = season[1]
                entry['region'] = mov['region']
                entry['dim_channel_id'] = mov['dim_channel_id']
                entry['scenario'] = 'conservative'
                entry['gross_sales_index'] = 1
                entry['gross_sales_init'] = mov['salesvalue']
                entry['gross_sales'] = entry['gross_sales_init']
                entry['discounts'] = 0
                entry['returns'] = 0
                entry['sales_units_init'] = mov['units']
                entry['sales_units'] = entry['sales_units_init']
                if entry['sales_units'] != 0:
                    entry['gross_sales_per_unit'] = entry['gross_sales'] / entry['sales_units']
                else:
                    entry['gross_sales_per_unit'] = entry['gross_sales']
                entry['sell_through_ratio'] = 1
                entry['net_sales'] = entry['gross_sales']
                entry['sell_in'] = entry['net_sales']
                entry['markup'] = 1
                entry['gross_margin_percentage'] = 0
                entry['gross_margin'] = 0
                entry['buying_budget'] = entry['sell_in']
                entry['gmroi_percentage_target'] = 0
                entry['beginning_season_inventory'] = mov['unitonhand_inventory']
                entry['markdown'] = 0
                entry['ending_season_inventory'] = entry['net_sales'] - entry['beginning_season_inventory']
                if entry['sales_units'] != 0:
                    entry['asp'] = entry['gross_sales'] / entry['sales_units']
                else:
                    entry['asp'] = entry['gross_sales']
                entry['average_cost_of_inventory'] = 0
                entry['intake_beginning_of_season'] = 0
    #             entry['mix'] = None
                if season in seasons[:2]:
                    entry['row_styling'] = None
                else:
                    entry['row_styling'] = 'highlight'

                # Convert floats to int
                for k,v in entry.items():
                    if k in ('gross_sales_per_unit', 'dim_channel_id', 'sales_year'):
                        entry[k] = int(round(v,0))

                # Check if record already exist in database
                record = existing.get((entry['sales_year'], entry['sales_season'], entry['region'], entry['dim_channel_id'], entry['scenario']))

                if record is not None:
                    update_count += 1

                    # Update record
                    v = Decimal(entry['gross_sales_init'])
                    setattr(record, 'gross_sales_init', v)
                    v = Decimal(entry['gross_sales_init']) * getattr(record, 'gross_sales_index')
                    setattr(record, 'gross_sales', v)
                    v = getattr(record, 'gross_sales') - getattr(record, 'discounts') - getattr(record, 'returns')
                    setattr(record, 'net_sales', v)
                    v = getattr(record, 'net_sales') * getattr(record, 'sell_through_ratio')
                    setattr(record, 'sell_in', v)
                    v = getattr(record, 'net_sales') * getattr(record, 'gross_margin_percentage')
                    setattr(record, 'gross_margin', v)
                    if getattr(record, 'markup') != 0:
                        v = getattr(record, 'sell_in') / getattr(record, 'markup')
                    else:
                        v = getattr(record, 'sell_in')
                    setattr(record, 'buying_budget', v)
                    v = Decimal(entry['beginning_season_inventory'])
                    setattr(record, 'beginning_season_inventory', v)
                    v = getattr(record, 'net_sales') - getattr(record, 'beginning_season_inventory') - getattr(record, 'markdown')
                    setattr(record, 'ending_season_inventory', v)
                    if getattr(record, 'sales_units') != 0 and getattr(record, 'sales_units') is not None:
                        v = getattr(record, 'gross_sales') / getattr(record, 'sales_units')
                    else:
                        v = getattr(record, 'gross_sales')
                    setattr(record, 'asp', v)
                    v = getattr(record, 'gross_margin') * getattr(record, 'gmroi_percentage_target')
                    setattr(record, 'average_cost_of_inventory', v)
                    v = entry['row_styling']
                    setattr(record, 'row_styling', v)
                else:
                    to_insert.append(dbo.app_dms_strategicsalesplan(**entry))

            print('Updated:', update_count, '| To Insert:', len(to_insert))
        session.commit()

    # Only add those posts which did not exist in the database
    session.bulk_save_objects(to_insert)

    # Now we commit our modifications (merges) and inserts (adds) to the database!
    session.commit()

    print('Updated:', update_count, 'Inserted:', len(to_insert))

    # Update mix
    for season in seasons:
        records = session.query(dbo.app_dms_strategicsalesplan).filter(
            dbo.app_dms_strategicsalesplan.sales_year == season[0]
        ).all()

        # Get sum
        m = sum([record.gross_sales_init for record in records])

        # Get percentage
        mix = list()
        for record in records:
            mix.append(record.gross_sales_init/m)

        # Update mix
        for record, record_mix in zip(records, mix):
            setattr(record, 'sales_year_mix', record_mix)

    session.commit()
