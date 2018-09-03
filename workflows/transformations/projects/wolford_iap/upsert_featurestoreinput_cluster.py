import pandas as pd
from decimal import *
from .clustering import clustering

def upsert_featurestoreinput_cluster(session, dbo, user_input):

    # Query all entries already existing
    existing_objects = session.query(dbo.app_dms_featurestoreinput).all()
    existing = {(o.dim_store_id, o.dim_iapfilter_id):o for o in existing_objects}

    # We loop by dimaipfilter to avoid querring fact movements all at once
    dimaipfilter = session.query(dbo.app_dms_dimiapfilter).all()

    total_update = 0

    for iapfilter in dimaipfilter:
        # Run clustering for given iapfilter
        df = clustering(session, dbo, user_input, iapfilter.id, iapfilter.dim_channel_id)

        # Build entries based on existing ones
        for idx, row in df.iterrows():
            record = existing.get((row['dim_store_id'], iapfilter.id))

            if getattr(record, 'cluster_user') == getattr(record, 'cluster_ai'):
                record.cluster_ai = row['cluster_label']
                record.cluster_user = row['cluster_label']
            else:
                record.cluster_ai = row['cluster_label']

        session.commit()
        total_update += df.shape[0]
        print('Updated:', df.shape[0])
        print('\n= Cluster Distribution =')
        print(df['cluster_label'].value_counts())

    # Now we commit our modifications (merges) and inserts (adds) to the database!
    session.commit()

    print('Total Updated:', total_update)
