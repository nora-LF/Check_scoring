# after data retrival add columns and create features from the same table
# if required

import pandas as pd
import lookup

# veri envanteri
envanter = pd.read_excel(lookup.path_envanter,
                         sheet_name='veri_envanteri')


def create_data(df):

    print('Creating data in %s ... '%df.name, end=' ')
    if(df.name == 'tableA'):

        df.name = 'tableA'

    if(df.name == 'tableB'):
    
        DB_tablo_name = lookup.db_names['tableB']
        df_veri = envanter[envanter['tablo'] == DB_tablo_name]
        df_veri = df_veri[df_veri['in_query'] == 1]
        cols = df_veri['veri']
        
        if('risk_rapor' in cols):
        # not complete
            df = df
            
            
        df.name = 'tableB'

    if(df.name == 'tableB'):
        def populate_params(df:pd.DataFrame):
            
            df['toplam_limit'] = df[df.columns[df.columns.str.endswith(\
                                            pat='_LIMIT')]].sum(axis=1)
            df['toplam_risk'] = df[df.columns[df.columns.str.endswith(\
                                            pat='_toplam_risk')]].sum(axis=1)
            df['toplam_limit_adet'] = df[df.columns[df.columns.str.endswith(\
                                            pat='_limit_adet')]].sum(axis=1)
            df['toplam_risk_adet'] = df[df.columns[df.columns.str.endswith(\
                                            pat='_risk_adet')]].sum(axis=1)
            df['faiz_toplam'] = df[df.columns[df.columns.str.endswith(\
                                            pat='_faiz_tahakkuk')]].sum(axis=1)
            df['toplam_limit_kullanim'] = df['toplam_risk']/df['toplam_limit']
            df['trend_10X_15X_faiz_tahakkuk'] = df['D_1_10X_15X_faiz_tahakkuk']/df['D_13_10X_15X_faiz_tahakkuk']
            df['trend_10X_15X_toplam_risk'] = df['D_1_10X_15X_toplam_risk']/df['D_13_10X_15X_toplam_risk']
            df['trend_70X_75X_toplam_risk'] = df['D_1_70X_75X_toplam_risk']/df['D_13_70X_75X_toplam_risk']
            neg_list_col = ['D_1_30X_35X_toplam_risk', 'D_1_31X_toplam_risk',
                    'D_1_66X_67X_toplam_risk', 'D_1_76X_77X_toplam_risk', 
                    'D_1_11X_16X_toplam_risk','D_1_21X_26X_toplam_risk']
            df['neg_risk_memzuc'] = df[[colName for x in neg_list_col for colName in df.columns if colName.endswith(x)]].sum(axis=1)
            
            return df
        
        df = populate_memzuc_params(df)
        
        df.name = 'memzuc'

    if(df.name == 'all'):
    
        # add columns (new dates)
        cols = {'col1':'col_1',
                'col2':'col_2'}
                
        for c in cols.keys():
            if(c in df.columns):
                df[cols[c]] = (df['islem_tar'] - df[c]).dt.days.\
                                       astype(pd.Int64Dtype())
                                       
        # one-hot encode
        df = pd.concat([df, pd.get_dummies(df['banka_kodu'], 
                                           prefix='bank')],
                       axis=1)
                       
        df['kes_nace'] = df['kes_nace'].astype(str).str[0:2]
        
        df = pd.concat([df, pd.get_dummies(df['kes_nace'], 
                                          prefix='nace')],
                       axis=1)
        if('nace_None' in df.columns):
            df.drop(columns=['nace_None'], inplace=True)
        if('nace_-1' in df.columns):
            df.drop(columns=['nace_-1'], inplace=True)
            
        df = pd.concat([df, pd.get_dummies(df['kes_tur'], 
                                           prefix='tur')],
                       axis=1)
        if('tur_None' in df.columns):
            df.drop(columns=['tur_None'], inplace=True)
            
        df = pd.concat([df, pd.get_dummies(df['il'],
                        prefix='il')],
                       axis=1)
        if('il_None' in df.columns):
            df.drop(columns=['il_None'], inplace=True)
        # karsiliksiz durum
        
        df.name = 'all'
        
    print('done!')
    return df




