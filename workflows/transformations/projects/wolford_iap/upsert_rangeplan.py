import pandas as pd

def upsert_rangeplan(session, dbo):

    # Queries
    query = session.query(dbo.app_dms_rangearchitecture)
    rangearchitecture = pd.read_sql(query.statement, query.session.bind)

    query = session.query(dbo.app_dms_rangemaster)
    rangemaster = pd.read_sql(query.statement, query.session.bind)

    # Transformations
    product_division = rangearchitecture.groupby('product_category').first()['product_division'].reset_index()

    raw_data = rangemaster.merge(rangearchitecture, on=['product_category', 'product_division', 'dim_iapfilter_id'], how='left')

    count_styles = raw_data.groupby(['product_category', 'product_essential_trend', 'product_basic_fashion', 'dim_iapfilter_id', 'style_number']).first(
    ).groupby(['product_category', 'product_essential_trend', 'product_basic_fashion', 'dim_iapfilter_id']).count().reset_index()

    count_styles_colour = raw_data.groupby(['product_category', 'product_essential_trend', 'product_basic_fashion', 'dim_iapfilter_id', 'style_number', 'colour_number']).first(
    ).groupby(['product_category', 'product_essential_trend', 'product_basic_fashion', 'dim_iapfilter_id']).count().reset_index()

    rangearchitecture['style_B'] = rangearchitecture['range_width_style_ly_essential_basic'] + rangearchitecture['range_width_style_ly_trend_basic']
    rangearchitecture['style_F'] = rangearchitecture['range_width_style_ly_essential_fashion'] + rangearchitecture['range_width_style_ly_trend_fashion']
    rangearchitecture['colour_B'] = rangearchitecture['range_width_style_colour_ly_essential_basic'] + rangearchitecture['range_width_style_colour_ly_trend_basic']
    rangearchitecture['colour_F'] = rangearchitecture['range_width_style_colour_ly_essential_fashion'] + rangearchitecture['range_width_style_colour_ly_trend_fashion']

    key_fields = ['product_category', 'product_division', 'product_essential_trend', 'product_basic_fashion', 'dim_iapfilter_id']
    data = raw_data.groupby(key_fields).first().reset_index()

    # List of entries to insert intod database
    to_insert = list()
    update_count = 0

    # Query all entries already existing
    existing_objects = session.query(dbo.app_dms_rangeplan).all()
    existing = {(o.product_category, o.product_essential_trend, o.product_basic_fashion, o.dim_iapfilter_id):o for o in existing_objects}

    for category, division, essential_trend, basic_fashion, dim_iapfilter_id in data[key_fields].values:

        # Create entry
        entry = dict()
        entry['product_category'] = category
        entry['product_division'] = division
        entry['product_essential_trend'] = essential_trend
        entry['product_basic_fashion'] = basic_fashion
        entry['dim_iapfilter_id'] = dim_iapfilter_id
        entry['range_width_style_py_rangearchitecture'] = 0
        entry['range_width_style_colour_py_rangearchitecture'] = 0
        entry['range_width_style_py_rangemaster'] = 0
        entry['range_width_style_colour_py_rangemaster'] = 0

        r = rangearchitecture[(rangearchitecture['product_category'] == category)
                               & (rangearchitecture['product_division'] == division)
                               & (rangearchitecture['dim_iapfilter_id'] == dim_iapfilter_id)]
        if len(r) > 0:
            entry['range_width_style_py_rangearchitecture'] = r['style_' + basic_fashion].iloc[0]

        r = rangearchitecture[(rangearchitecture['product_category'] == category)
                               & (rangearchitecture['product_division'] == division)
                               & (rangearchitecture['dim_iapfilter_id'] == dim_iapfilter_id)]
        if len(r) > 0:
            entry['range_width_style_colour_py_rangearchitecture'] = r['colour_' + basic_fashion].iloc[0]

        r = count_styles[(count_styles['product_category'] == category)
                         & (count_styles['product_essential_trend'] == essential_trend)
                         & (count_styles['product_basic_fashion'] == basic_fashion)
                         & (count_styles['dim_iapfilter_id'] == dim_iapfilter_id)]
        if len(r) > 0:
            entry['range_width_style_py_rangemaster'] = r['id_x'].iloc[0]

        r = count_styles_colour[(count_styles['product_category'] == category)
                                 & (count_styles['product_essential_trend'] == essential_trend)
                                 & (count_styles['product_basic_fashion'] == basic_fashion)
                                 & (count_styles['dim_iapfilter_id'] == dim_iapfilter_id)]
        if len(r) > 0:
            entry['range_width_style_colour_py_rangemaster'] = r['id_x'].iloc[0]

        # Convert floats to int if any
        for k,v in entry.items():
            if k in ('range_width_style_py_rangearchitecture', 'range_width_style_colour_py_rangearchitecture',
                         'range_width_style_py_rangemaster', 'range_width_style_colour_py_rangemaster'):
                entry[k] = int(round(v,0))

        # Check if record is already in database
        record = existing.get((category, essential_trend, basic_fashion, dim_iapfilter_id))

        if record is not None:
            # Update record
            for k, v in entry.items():
                setattr(record, k, v)

            update_count += 1
        else:
            to_insert.append(dbo.app_dms_rangeplan(**entry))

    # Only add those posts which did not exist in the database
    session.bulk_save_objects(to_insert)

    # Now we commit our modifications (merges) and inserts (adds) to the database!
    session.commit()

    print('Updated:', update_count, '| Inserted:', len(to_insert))
