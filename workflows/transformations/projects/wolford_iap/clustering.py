import pandas as pd
import numpy as np
import copy
from decimal import *
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import dendrogram, linkage, cophenet, fcluster
from scipy.cluster.hierarchy import cophenet
from scipy.spatial.distance import pdist
from sklearn.decomposition import PCA
from sklearn import metrics
from mpl_toolkits.mplot3d import Axes3D
from collections import Counter

def clustering(session, dbo, user_input, dim_iapfilter_id, dim_channel_id, debug = False):

    # == Query app_dms_featurestoreinput ==
    query = session.query(dbo.app_dms_featurestoreinput)
    featurestoreinput = pd.read_sql(query.statement, query.session.bind)

    q = session.query(
        dbo.app_dms_featurestoreinput,
        dbo.app_dms_dimstore,
        dbo.app_dms_dimlocation
    )
    items = q.filter(
        dbo.app_dms_featurestoreinput.dim_store_id == dbo.app_dms_dimstore.id,
        dbo.app_dms_dimlocation.id == dbo.app_dms_dimstore.dim_location_id,
        dbo.app_dms_featurestoreinput.dim_iapfilter_id == dim_iapfilter_id
    )
    df_store = pd.read_sql(items.statement, items.session.bind)

    df_clustering = df_store[df_store['dim_channel_id'] == dim_channel_id]
    df_clustering = df_clustering[user_input['store_fields']]


    # == Pre-processing data ==

    # Exclude if 50% or more of rows are NULL
    # Exclusion of text feature if > 95% of rows have different value (e.g. store name) Goal is to eliminate features without statistical significance)
    exclusion_threshold_null = 0.5
    exclusion_threshold_unique = 0.95

    if debug:
        print("_"*80)
        print("Column          \tnull ratio\tunique ratio\tdtype")

    drop_feature = list()
    for feature in df_clustering.columns:

        if df_clustering[feature].dtype == 'object':
            df_clustering.loc[df_clustering[feature]=='',feature] = np.nan

        ratio_null = df_clustering[feature].isnull().sum()/float(len(df_clustering))
        ratio_unique = len(df_clustering[feature].unique())/float(len(df_clustering))

        if ratio_null > exclusion_threshold_null:
            drop_feature.append(feature)

        if df_clustering[feature].dtype == 'object' and ratio_unique > exclusion_threshold_unique:
            drop_feature.append(feature)

        if debug:
            print("%20s\t%f\t%f\t%s" % (feature[:20], ratio_null, ratio_unique, df_clustering[feature].dtype))

    if debug:
        print("_"*80)
        print("Exclude: ", drop_feature)

    df_clustering = df_clustering.drop(drop_feature, axis=1)

    # Transform each category quantities into ratios (to avoid quantity to be repeated and skew data when clustering)
    fields = ['sales_lingerie', 'sales_legwear', 'sales_ready_to_wear', 'sales_accessories', 'sales_adv_promotion']
    series_sum = df_clustering[fields].sum(axis=1)
    for field in fields:
        if field in df_clustering:
            df_clustering[field] = df_clustering[field] / series_sum

    # Smoothen Quantities with Log
    labels_to_convert = ['sku_count', 'net_retail_sales_in_eur_ty', 'average_monthly_sales_for_ty']
    for label in labels_to_convert:
        if label in df_clustering:
            df_clustering[label] = np.log10(df_clustering[label])

    # Insert Mean In Missing Data
    exceptions = ['store_tier']
    for column in df_clustering.columns:
        if df_clustering[column].dtype in ('float', 'int') and column not in exceptions:
            mean = df_clustering[column].mean()
            df_clustering[column].fillna(mean,inplace=True)

    # Transform text columns into dummy columns
    text_columns = ['region', 'country', 'store_tier']
    for column in text_columns:
        if column in df_clustering:
            for label in df_clustering[column].dropna().unique():
                df_clustering[label] = df_clustering[column] == label

    df_clustering = df_clustering.drop(text_columns, axis=1)

    # Continuous Variables Scaling
    continuous_all = {'store_size', 'net_retail_sales_in_eur_ty', 'average_monthly_sales_for_ty',
        'sku_count', 'sales_lingerie', 'sales_legwear', 'sales_ready_to_wear', 'sales_accessories',
        'sales_adv_promotion'}
    continuous = list(set(df_clustering.columns) & continuous_all)

    data_continuous = list()
    for _, row in df_clustering[continuous].iterrows():
        data_continuous.append(row.values)

    samples_continuous = np.array(data_continuous)

    # from sklearn.preprocessing import MinMaxScaler
    # samples_continuous = MinMaxScaler().fit_transform(samples_continuous)

    samples_continuous = StandardScaler().fit_transform(samples_continuous)

    # Binary Variables
    data_binary = list()
    for _, row in df_clustering.drop(continuous, axis=1).iterrows():
        data_binary.append(row.values)

    samples_binary = np.array(data_binary)
    samples = np.concatenate((samples_continuous, samples_binary), axis=1)

    features = {idx: feature for idx, feature in enumerate(df_clustering.columns)}

    print('Samples shape:', samples.shape)

    # == Clustering ==
    data = samples
    Z = linkage(data, 'single')

    # max_d = 75
    # labels = fcluster(Z, max_d, criterion='distance')

    k = user_input['cluster_number']
    labels = fcluster(Z, k, criterion='maxclust')

    # Adding cluster labels to df
    labels_hierarchy = labels
    df = copy.deepcopy(df_store)
    df['cluster'] = labels_hierarchy

    # Change cluster labels based on cluster size
    order_cluster_mapping = list(df['cluster'].value_counts().index)
    df['cluster'] = df['cluster'].apply(order_cluster_mapping.index)

    # Add cluster label
    df['cluster_label'] = df['cluster'].map(pd.Series(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')))

    # Show metrics
    silhouette = metrics.silhouette_score(data, labels, metric='euclidean')
    print("silhouette:", silhouette)

    df.groupby('cluster')['sku_count'].agg(['sum','count'])

    return df
