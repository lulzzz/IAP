import pandas as pd

def upsert_rangeassortment(session, dbo):

    # Queries
    query = session.query(dbo.app_dms_featureproductinputbycluster, dbo.app_dms_dimproduct).filter(
    dbo.app_dms_featureproductinputbycluster.dim_product_id == dbo.app_dms_dimproduct.id)
    data_raw = pd.read_sql(query.statement, query.session.bind)

    count_styles = data_raw.groupby(['category', 'cluster', 'essential_trend', 'basic_fashion', 'dim_iapfilter_id', 'style']).first(
    ).groupby(['category', 'cluster', 'essential_trend', 'basic_fashion', 'dim_iapfilter_id']).count().reset_index()

    count_styles_colour = data_raw.groupby(['category', 'cluster', 'essential_trend', 'basic_fashion', 'dim_iapfilter_id', 'style', 'colour']).first(
    ).groupby(['category', 'cluster', 'essential_trend', 'basic_fashion', 'dim_iapfilter_id']).count().reset_index()

    key_fields = ['cluster', 'category', 'division', 'essential_trend', 'basic_fashion', 'dim_iapfilter_id']
    data = data_raw.groupby(key_fields).first().reset_index()

    # List of entries to insert intod database
    to_insert = list()
    update_count = 0

    # Query all entries already existing
    existing_objects = session.query(dbo.app_dms_rangeassortment).all()
    existing = {(o.cluster_user, o.product_category, o.product_division, o.product_essential_trend, o.product_basic_fashion, o.dim_iapfilter_id):o for o in existing_objects}

    for cluster, category, division, essential_trend, basic_fashion, dim_iapfilter_id in data[key_fields].values:

        # Create entry
        entry = dict()
        entry['cluster_user'] = cluster
        entry['product_category'] = category
        entry['product_division'] = division
        entry['product_essential_trend'] = essential_trend
        entry['product_basic_fashion'] = basic_fashion
        entry['dim_iapfilter_id'] = dim_iapfilter_id
        entry['range_width_style_ly_storecluster'] = 0
        entry['range_width_style_colour_ly_storecluster'] = 0
        entry['range_width_style_py'] = 0
        entry['range_width_style_colour_py'] = 0

        r = count_styles[(count_styles['cluster'] == cluster)
                         & (count_styles['category'] == category)
                         & (count_styles['essential_trend'] == essential_trend)
                         & (count_styles['basic_fashion'] == basic_fashion)
                         & (count_styles['dim_iapfilter_id'] == dim_iapfilter_id)]
        if len(r) > 0:
            entry['range_width_style_ly_storecluster'] = r['dim_product_id'].iloc[0]
            entry['range_width_style_py'] = entry['range_width_style_ly_storecluster']

        r = count_styles_colour[(count_styles['cluster'] == cluster)
                                 & (count_styles['category'] == category)
                                 & (count_styles['essential_trend'] == essential_trend)
                                 & (count_styles['basic_fashion'] == basic_fashion)
                                 & (count_styles['dim_iapfilter_id'] == dim_iapfilter_id)]
        if len(r) > 0:
            entry['range_width_style_colour_ly_storecluster'] = r['dim_product_id'].iloc[0]
            entry['range_width_style_colour_py'] = entry['range_width_style_colour_ly_storecluster']

        # Convert floats to int if any
        for k,v in entry.items():
            if k in ('range_width_style_ly_storecluster', 'range_width_style_colour_ly_storecluster',
                         'range_width_style_py', 'range_width_style_colour_py'):
                entry[k] = int(round(v,0))

        # Check if record is already in database
        record = existing.get((cluster, category, division, essential_trend, basic_fashion, dim_iapfilter_id))

        if record is not None:
            # Update record
            for k, v in entry.items():
                if k not in ('range_width_style_py', 'range_width_style_colour_py'):
                    setattr(record, k, v)
                elif k == 'range_width_style_py' and getattr(record, k) == getattr(record, 'range_width_style_ly_storecluster'):
                    setattr(record, k, v)
                elif k == 'range_width_style_colour_py' and getattr(record, k) == getattr(record, 'range_width_style_colour_ly_storecluster'):
                    setattr(record, k, v)

            update_count += 1
        else:
            to_insert.append(dbo.app_dms_rangeassortment(**entry))

    # Only add those posts which did not exist in the database
    session.bulk_save_objects(to_insert)

    # Now we commit our modifications (merges) and inserts (adds) to the database!
    session.commit()

    print('Updated:', update_count, '| Inserted:', len(to_insert))
