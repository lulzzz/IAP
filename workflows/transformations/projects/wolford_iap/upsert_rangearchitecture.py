import pandas as pd

def upsert_rangearchitecture(session, dbo):

    query = session.query(dbo.app_dms_dimproduct)
    products = pd.read_sql(query.statement, query.session.bind)

    query = session.query(dbo.app_dms_dimstore)
    stores = pd.read_sql(query.statement, query.session.bind)

    # Query all entries already existing
    existing_objects = session.query(dbo.app_dms_rangearchitecture).all()
    existing = {(o.product_category, o.product_division, o.dim_iapfilter_id):o for o in existing_objects}

    # We loop by dimaipfilter to avoid querring fact movements all at once
    dimaipfilter = session.query(dbo.app_dms_dimiapfilter).all()

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

        # Join with products and aggregate
        movements = movements.merge(products, how='left', left_on='dim_product_id', right_on='id')

        count_styles = movements.groupby(['category', 'essential_trend', 'basic_fashion', 'style']).count(
        ).groupby(['category', 'essential_trend', 'basic_fashion']).count()['units'].reset_index()

        count_styles_colour = movements.groupby(['category', 'essential_trend', 'basic_fashion', 'style', 'colour']).count(
        ).groupby(['category', 'essential_trend', 'basic_fashion']).count()['units'].reset_index()

        sum_units = movements.groupby(['category', 'essential_trend', 'basic_fashion']).sum()['units'].reset_index()

        colour_count = movements.groupby(['category', 'essential_trend', 'basic_fashion', 'style', 'colour']).count(
        ).groupby(['category', 'essential_trend', 'basic_fashion', 'style']).count(
        ).groupby(['category', 'essential_trend', 'basic_fashion']).mean()['units'].reset_index()

        sum_mov = movements.groupby('category').sum().reset_index()

        # Build entries based on existing ones

        for cat, div in movements.groupby('category').first().reset_index()[['category', 'division']].values:
            record = existing.get((cat, div, iapfilter.id))
            if record is not None:
                # Update record

                if record.range_width_style_py_essential_basic == record.range_width_style_ly_essential_basic:
                    record.range_width_style_ly_essential_basic = get_from(count_styles, cat, **essential_basic)
                    record.range_width_style_py_essential_basic = record.range_width_style_ly_essential_basic
                else:
                    record.range_width_style_ly_essential_basic = get_from(count_styles, cat, **essential_basic)

                if record.range_width_style_py_essential_fashion == record.range_width_style_ly_essential_fashion:
                    record.range_width_style_ly_essential_fashion = get_from(count_styles, cat, **essential_fashion)
                    record.range_width_style_py_essential_fashion = record.range_width_style_ly_essential_fashion
                else:
                    record.range_width_style_ly_essential_fashion = get_from(count_styles, cat, **essential_fashion)

                if record.range_width_style_py_trend_basic == record.range_width_style_ly_trend_basic:
                    record.range_width_style_ly_trend_basic = get_from(count_styles, cat, **trend_basic)
                    record.range_width_style_py_trend_basic = record.range_width_style_ly_trend_basic
                else:
                    record.range_width_style_ly_trend_basic = get_from(count_styles, cat, **trend_basic)

                if record.range_width_style_py_trend_fashion == record.range_width_style_ly_trend_fashion:
                    record.range_width_style_ly_trend_fashion = get_from(count_styles, cat, **trend_fashion)
                    record.range_width_style_py_trend_fashion = record.range_width_style_ly_trend_fashion
                else:
                    record.range_width_style_ly_trend_fashion = get_from(count_styles, cat, **trend_fashion)


                record.range_width_style_ly_total = record.range_width_style_ly_essential_basic \
                                                    + record.range_width_style_ly_essential_fashion \
                                                    + record.range_width_style_ly_trend_basic \
                                                    + record.range_width_style_ly_trend_fashion


                record.range_width_style_py_total = record.range_width_style_py_essential_basic \
                                                    + record.range_width_style_py_essential_fashion \
                                                    + record.range_width_style_py_trend_basic \
                                                    + record.range_width_style_py_trend_fashion

                record.range_width_style_ly_essential_basic_avg_colour_count = get_from(colour_count, cat, **essential_basic)
                record.range_width_style_ly_trend_basic_avg_colour_count = get_from(colour_count, cat, **trend_basic)
                record.range_width_style_ly_trend_fashion_avg_colour_count = get_from(colour_count, cat, **trend_fashion)
                record.range_width_style_ly_essential_fashion_avg_colour_count = get_from(colour_count, cat, **essential_fashion)

                if record.range_width_style_colour_py_essential_basic == record.range_width_style_colour_ly_essential_basic:
                    record.range_width_style_colour_ly_essential_basic = get_from(count_styles_colour, cat, **essential_basic)
                    record.range_width_style_colour_py_essential_basic = record.range_width_style_colour_ly_essential_basic
                else:
                    record.range_width_style_colour_ly_essential_basic = get_from(count_styles_colour, cat, **essential_basic)

                if record.range_width_style_colour_py_essential_fashion == record.range_width_style_colour_ly_essential_fashion:
                    record.range_width_style_colour_ly_essential_fashion = get_from(count_styles_colour, cat, **essential_fashion)
                    record.range_width_style_colour_py_essential_fashion = record.range_width_style_colour_ly_essential_fashion
                else:
                    record.range_width_style_colour_ly_essential_fashion = get_from(count_styles_colour, cat, **essential_fashion)

                if record.range_width_style_colour_py_trend_basic == record.range_width_style_colour_ly_trend_basic:
                    record.range_width_style_colour_ly_trend_basic = get_from(count_styles_colour, cat, **trend_basic)
                    record.range_width_style_colour_py_trend_basic = record.range_width_style_colour_ly_trend_basic
                else:
                    record.range_width_style_colour_ly_trend_basic = get_from(count_styles_colour, cat, **trend_basic)

                if record.range_width_style_colour_py_trend_fashion == record.range_width_style_colour_ly_trend_fashion:
                    record.range_width_style_colour_ly_trend_fashion = get_from(count_styles_colour, cat, **trend_fashion)
                    record.range_width_style_colour_py_trend_fashion = record.range_width_style_colour_ly_trend_fashion
                else:
                    record.range_width_style_colour_ly_trend_fashion = get_from(count_styles_colour, cat, **trend_fashion)


                record.range_width_style_colour_ly_total = record.range_width_style_colour_ly_essential_basic \
                                                            + record.range_width_style_colour_ly_essential_fashion \
                                                            + record.range_width_style_colour_ly_trend_basic \
                                                            + record.range_width_style_colour_ly_trend_fashion


                record.range_width_style_colour_py_total = record.range_width_style_colour_py_essential_basic \
                                                        + record.range_width_style_colour_py_essential_fashion \
                                                        + record.range_width_style_colour_py_trend_basic \
                                                        + record.range_width_style_colour_py_trend_fashion

                record.range_sales_ly_essential_basic = get_from(sum_units, cat, **essential_basic)
                record.range_sales_ly_essential_fashion = get_from(sum_units, cat, **essential_fashion)
                record.range_sales_ly_trend_basic = get_from(sum_units, cat, **trend_basic)
                record.range_sales_ly_trend_fashion = get_from(sum_units, cat, **trend_fashion)
                record.range_sales_ly_total = record.range_sales_ly_essential_basic \
                                                + record.range_sales_ly_essential_fashion \
                                                + record.range_sales_ly_trend_basic \
                                                + record.range_sales_ly_trend_fashion


                if record.range_effectiveness_style_py_essential_basic == record.range_effectiveness_style_ly_essential_basic:
                    if record.range_width_style_ly_essential_basic == 0:
                        record.range_effectiveness_style_ly_essential_basic = record.range_sales_ly_essential_basic
                    else:
                        record.range_effectiveness_style_ly_essential_basic = int(round(record.range_sales_ly_essential_basic / record.range_width_style_ly_essential_basic, 0))
                    record.range_effectiveness_style_py_essential_basic = record.range_effectiveness_style_ly_essential_basic
                else:
                    if record.range_width_style_ly_essential_basic == 0:
                        record.range_effectiveness_style_ly_essential_basic = record.range_sales_ly_essential_basic
                    else:
                        record.range_effectiveness_style_ly_essential_basic = int(round(record.range_sales_ly_essential_basic / record.range_width_style_ly_essential_basic, 0))

                if record.range_effectiveness_style_py_essential_fashion == record.range_effectiveness_style_ly_essential_fashion:
                    if record.range_width_style_ly_essential_fashion == 0:
                        record.range_effectiveness_style_ly_essential_fashion = record.range_sales_ly_essential_fashion
                    else:
                        record.range_effectiveness_style_ly_essential_fashion = int(round(record.range_sales_ly_essential_fashion / record.range_width_style_ly_essential_fashion, 0))
                    record.range_effectiveness_style_py_essential_fashion = record.range_effectiveness_style_ly_essential_fashion
                else:
                    if record.range_width_style_ly_essential_fashion == 0:
                        record.range_effectiveness_style_ly_essential_fashion = record.range_sales_ly_essential_fashion
                    else:
                        record.range_effectiveness_style_ly_essential_fashion = int(round(record.range_sales_ly_essential_fashion / record.range_width_style_ly_essential_fashion, 0))

                if record.range_effectiveness_style_py_trend_basic == record.range_effectiveness_style_ly_trend_basic:
                    if record.range_width_style_ly_trend_basic == 0:
                        record.range_effectiveness_style_ly_trend_basic = record.range_sales_ly_trend_basic
                    else:
                        record.range_effectiveness_style_ly_trend_basic = int(round(record.range_sales_ly_trend_basic / record.range_width_style_ly_trend_basic, 0))
                    record.range_effectiveness_style_py_trend_basic = record.range_effectiveness_style_ly_trend_basic
                else:
                    if record.range_width_style_ly_trend_basic == 0:
                        record.range_effectiveness_style_ly_trend_basic = record.range_sales_ly_trend_basic
                    else:
                        record.range_effectiveness_style_ly_trend_basic = int(round(record.range_sales_ly_trend_basic / record.range_width_style_ly_trend_basic, 0))

                if record.range_effectiveness_style_py_trend_fashion == record.range_effectiveness_style_ly_trend_fashion:
                    if record.range_width_style_ly_trend_fashion == 0:
                        record.range_effectiveness_style_ly_trend_fashion = record.range_sales_ly_trend_fashion
                    else:
                        record.range_effectiveness_style_ly_trend_fashion = int(round(record.range_sales_ly_trend_fashion / record.range_width_style_ly_trend_fashion, 0))
                    record.range_effectiveness_style_py_trend_fashion = record.range_effectiveness_style_ly_trend_fashion
                else:
                    if record.range_width_style_ly_trend_fashion == 0:
                        record.range_effectiveness_style_ly_trend_fashion = record.range_sales_ly_trend_fashion
                    else:
                        record.range_effectiveness_style_ly_trend_fashion = int(round(record.range_sales_ly_trend_fashion / record.range_width_style_ly_trend_fashion, 0))

                if record.range_effectiveness_style_py_total == record.range_effectiveness_style_ly_total:
                    record.range_effectiveness_style_py_total = int(round(record.range_sales_ly_total / record.range_width_style_py_total, 0))

                record.range_effectiveness_style_ly_total = record.range_effectiveness_style_ly_essential_basic \
                                                            + record.range_effectiveness_style_ly_essential_fashion \
                                                            + record.range_effectiveness_style_ly_trend_basic \
                                                            + record.range_effectiveness_style_ly_trend_fashion

                record.range_performance_ly = int(round(sum_mov[sum_mov['category'] == cat]['salesvalue'].iloc[0] / sum_mov[sum_mov['category'] == cat]['units'].iloc[0], 0))
                record.range_performance_py = int(round(sum_mov[sum_mov['category'] == cat]['salesvalue'].iloc[0] / sum_mov[sum_mov['category'] == cat]['units'].iloc[0], 0))

                update_count += 1

            else:
                entry = dict()

                # Create entry and append to insert
                entry['product_category'] = cat
                entry['product_division'] = div
                entry['dim_iapfilter_id'] = iapfilter.id

                entry['range_width_style_ly_essential_basic'] = get_from(count_styles, cat, **essential_basic)
                entry['range_width_style_ly_essential_fashion'] = get_from(count_styles, cat, **essential_fashion)
                entry['range_width_style_ly_trend_basic'] = get_from(count_styles, cat, **trend_basic)
                entry['range_width_style_ly_trend_fashion'] = get_from(count_styles, cat, **trend_fashion)
                entry['range_width_style_ly_total'] = entry['range_width_style_ly_essential_basic'] \
                                                    + entry['range_width_style_ly_essential_fashion'] \
                                                    + entry['range_width_style_ly_trend_basic'] \
                                                    + entry['range_width_style_ly_trend_fashion']

                entry['range_width_style_py_essential_basic'] = entry['range_width_style_ly_essential_basic']
                entry['range_width_style_py_essential_fashion'] = entry['range_width_style_ly_essential_fashion']
                entry['range_width_style_py_trend_basic'] = entry['range_width_style_ly_trend_basic']
                entry['range_width_style_py_trend_fashion'] = entry['range_width_style_ly_trend_fashion']
                entry['range_width_style_py_carry_over'] = 0
                entry['range_width_style_py_total'] = entry['range_width_style_ly_total']

                entry['range_width_style_ly_essential_basic_avg_colour_count'] = get_from(colour_count, cat, **essential_basic)
                entry['range_width_style_ly_trend_basic_avg_colour_count'] = get_from(colour_count, cat, **trend_basic)
                entry['range_width_style_ly_trend_fashion_avg_colour_count'] = get_from(colour_count, cat, **trend_fashion)
                entry['range_width_style_ly_essential_fashion_avg_colour_count'] = get_from(colour_count, cat, **essential_fashion)

                entry['range_width_style_colour_ly_essential_basic'] = get_from(count_styles_colour, cat, **essential_basic)
                entry['range_width_style_colour_ly_essential_fashion'] = get_from(count_styles_colour, cat, **essential_fashion)
                entry['range_width_style_colour_ly_trend_basic'] = get_from(count_styles_colour, cat, **trend_basic)
                entry['range_width_style_colour_ly_trend_fashion'] = get_from(count_styles_colour, cat, **trend_fashion)
                entry['range_width_style_colour_ly_total'] = entry['range_width_style_colour_ly_essential_basic'] \
                                                            + entry['range_width_style_colour_ly_essential_fashion'] \
                                                            + entry['range_width_style_colour_ly_trend_basic'] \
                                                            + entry['range_width_style_colour_ly_trend_fashion']

                entry['range_width_style_colour_py_essential_basic'] = entry['range_width_style_colour_ly_essential_basic']
                entry['range_width_style_colour_py_essential_fashion'] = entry['range_width_style_colour_ly_essential_fashion']
                entry['range_width_style_colour_py_trend_basic'] = entry['range_width_style_colour_ly_trend_basic']
                entry['range_width_style_colour_py_trend_fashion'] = entry['range_width_style_colour_ly_trend_fashion']
                entry['range_width_style_colour_py_carry_over'] = 0
                entry['range_width_style_colour_py_total'] = entry['range_width_style_colour_ly_total']

                entry['range_sales_ly_essential_basic'] = get_from(sum_units, cat, **essential_basic)
                entry['range_sales_ly_essential_fashion'] = get_from(sum_units, cat, **essential_fashion)
                entry['range_sales_ly_trend_basic'] = get_from(sum_units, cat, **trend_basic)
                entry['range_sales_ly_trend_fashion'] = get_from(sum_units, cat, **trend_fashion)
                entry['range_sales_ly_total'] = entry['range_sales_ly_essential_basic'] \
                                                + entry['range_sales_ly_essential_fashion'] \
                                                + entry['range_sales_ly_trend_basic'] \
                                                + entry['range_sales_ly_trend_fashion']

                if entry['range_width_style_ly_essential_basic'] == 0:
                    entry['range_effectiveness_style_ly_essential_basic'] = entry['range_sales_ly_essential_basic']
                else:
                    entry['range_effectiveness_style_ly_essential_basic'] = entry['range_sales_ly_essential_basic'] / entry['range_width_style_ly_essential_basic']

                if entry['range_width_style_ly_essential_fashion'] == 0:
                    entry['range_effectiveness_style_ly_essential_fashion'] = entry['range_sales_ly_essential_fashion']
                else:
                    entry['range_effectiveness_style_ly_essential_fashion'] = entry['range_sales_ly_essential_fashion'] / entry['range_width_style_ly_essential_fashion']

                if entry['range_width_style_ly_trend_basic'] == 0:
                    entry['range_effectiveness_style_ly_trend_basic'] = entry['range_sales_ly_trend_basic']
                else:
                    entry['range_effectiveness_style_ly_trend_basic'] = entry['range_sales_ly_trend_basic'] / entry['range_width_style_ly_trend_basic']

                if entry['range_width_style_ly_trend_fashion'] == 0:
                    entry['range_effectiveness_style_ly_trend_fashion'] = entry['range_sales_ly_trend_fashion']
                else:
                    entry['range_effectiveness_style_ly_trend_fashion'] = entry['range_sales_ly_trend_fashion'] / entry['range_width_style_ly_trend_fashion']


                entry['range_effectiveness_style_ly_total'] = entry['range_effectiveness_style_ly_essential_basic'] \
                                                            + entry['range_effectiveness_style_ly_essential_fashion'] \
                                                            + entry['range_effectiveness_style_ly_trend_basic'] \
                                                            + entry['range_effectiveness_style_ly_trend_fashion']

                entry['range_effectiveness_style_py_essential_basic'] = entry['range_effectiveness_style_ly_essential_basic']
                entry['range_effectiveness_style_py_essential_fashion'] = entry['range_effectiveness_style_ly_essential_fashion']
                entry['range_effectiveness_style_py_trend_basic'] = entry['range_effectiveness_style_ly_trend_basic']
                entry['range_effectiveness_style_py_trend_fashion'] = entry['range_effectiveness_style_ly_trend_fashion']
                entry['range_effectiveness_style_py_carry_over'] = 0
                entry['range_effectiveness_style_py_total'] = entry['range_effectiveness_style_ly_total']

                entry['range_performance_ly'] = sum_mov[sum_mov['category'] == cat]['salesvalue'].iloc[0] / sum_mov[sum_mov['category'] == cat]['units'].iloc[0]
                entry['range_performance_py'] = sum_mov[sum_mov['category'] == cat]['salesvalue'].iloc[0] / sum_mov[sum_mov['category'] == cat]['units'].iloc[0]

                # Convert floats to int
                for k,v in entry.items():
                    if k not in ('product_category', 'product_division', 'dim_iapfilter_id'):
                        entry[k] = int(round(v,0))

                to_insert.append(dbo.app_dms_rangearchitecture(**entry))

        session.commit()
        print('Updated:', update_count, '| To Insert:', len(to_insert))

    # Only add those posts which did not exist in the database
    session.bulk_save_objects(to_insert)

    # Now we commit our modifications (merges) and inserts (adds) to the database!
    session.commit()

    print('Updated:', update_count, '| Inserted:', len(to_insert))
