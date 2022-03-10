import psycopg2
import pandas as pd
import numpy as np
import lookup

# veri envanteri
envanter = pd.read_excel(lookup.path_envanter,
                         sheet_name='veri_envanteri')


###############################################################################
# TABLE A
DB_tablo_name = lookup.db_names['tableA']
df_veri = envanter[envanter['tablo'] == DB_tablo_name]
df_veri = df_veri[df_veri['in_query'] == 1]
cols = df_veri['veri']

query = '''select %s ...
           from %s
           ...
           '''\
               %(','.join(cols), DB_tablo_name)

tableA = (DB_tablo_name, query, cols)
###############################################################################
# TABLE B
DB_tablo_name = lookup.db_names['tableB']
cols = list(envanter[envanter['tablo'] == DB_tablo_name]\
              [envanter['in_query'] == 1]['veri'])

query = '''select %s from %s'''\
                 %(','.join(cols), DB_tablo_name)

tableB = (DB_tablo_name, query, cols)
###############################################################################
# TABLE C
DB_tablo_name = lookup.db_names['tableC']
df_veri = envanter[envanter['tablo'] == DB_tablo_name]
df_veri = df_veri[df_veri['in_query'] == 1]
cols = df_veri['veri']

query_part = list(set(cols))

if('LIMIT' in query_part):
    query_part.remove('LIMIT')
    query_part.append('"LIMIT"')

query_part = ','.join(query_part)

query = '''select %s from %s ...'''\
                 %(query_part, DB_tablo_name)

tableC = (DB_tablo_name, query, cols)
###############################################################################

###############################################################################
# data isimleri eşleştirme
data_dict = {'tableA':tableA, 'tableB':tableB, 'tableC':tableC}
###############################################################################


def retrieve_data(dataname=None, cols=None, data_source=None):

    if(data_source == 'csv'):
        
        columns = pd.read_csv(lookup.path_data_in_csv,
                              nrows=1).columns.tolist()

        date_cols = []
        dtypes = {}

        for c in columns:
            df_type = envanter[envanter['veri'] == c]
            data_type = df_type['veri_tipi']
            if(len(data_type) == 0):
                continue
            else:
                data_type = data_type.iloc[0]

            if(data_type == 'date'):
                date_cols.append(c)
            else:
                dtypes[c] = lookup.type_conversion[data_type]

        df = pd.read_csv(lookup.path_data_in_csv,
                         dtype=dtypes,
                         parse_dates=date_cols)
        df.name = 'all'
        
        return df


    table_name, query, columns = data_dict[dataname]

    connection = psycopg2.connect(user='aUser',
                              password='aPass',
                              host='IP',
                              port=0000,
                              database='dbName')
    date_cols = []
    #na_values = {}
    dtypes = {}

    if(cols == None):

        for c in columns:
            df_type = envanter[envanter['tablo'] == table_name]
            df_type = df_type[df_type['veri'] == c]
            data_type = df_type['veri_tipi'].iloc[0]
            #na_value = envanter[envanter['tablo'] == table_name][envanter['veri'] == c]['na_values'].iloc[0]
            #na_values[c] = na_value
            
            if(data_type == 'date'):
                date_cols.append(c)
            else:
                dtypes[c] = lookup.type_conversion[data_type]

    elif(cols == 'all'):
        query = '''select * from %s'''%table_name
    try:
        print('Getting data from %s ... '%table_name, end=' ')
        df = pd.read_sql_query(con = connection,
                               sql = query,
                               parse_dates=date_cols,
                               dtype=dtypes)
        print('done!')
        
    finally:
        connection.close()

    df.name = dataname
    
    return df

