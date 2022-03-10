import pandas as pd
import numpy as np
import constant_objects as cso # edit later

def check_2cols_tcvkn(col1, col2):
# col1 = tckimlik no
# col2 = vergi no
# returns tckn, vkn lists

    col1 = col1.astype(str)
    cols = col2.astype(str)
    vkn = []
    tckn = []

    for t, v in zip(col1, col2):
        if(pd.isna(v) and pd.isna(t)):
            tckn.append(np.nan)
            vkn.append(np.nan)
            continue
            
        if(pd.isna(v) and pd.notna(t)):
            
            if(' ' in t):
                t = t.replace(' ', '')
            if(not t.isdecimal()):
                tckn.append(np.nan)
                vkn.append(np.nan)
                continue

            if(len(t) == 11 and t[0] != '0'):
                tckn.append(t)
                vkn.append(np.nan)
            elif(len(t) == 10):
                tckn.append(np.nan)
                vkn.append(t)
            elif(len(t) == 9):
                tckn.append(np.nan)
                vkn.append('0' + t)
            elif(len(t) == 8):
                tckn.append(np.nan)
                vkn.append('00' + t)
            else:
                vkn.append(np.nan)
                tckn.append(np.nan)
        elif(pd.notna(v) and pd.isna(t)):
            if(' ' in v):
                v = v.replace(' ', '')
            if(not v.isdecimal()):
                tckn.append(np.nan)
                vkn.append(np.nan)
                continue
                
            if(len(v) == 11 and v[0] != '0'):
                tckn.append(v)
                vkn.append(np.nan)
            elif(len(v) == 10):
                tckn.append(np.nan)
                vkn.append(v)
            elif(len(v) == 9):
                tckn.append(np.nan)
                vkn.append('0' + v)
            elif(len(t) == 8):
                tckn.append(np.nan)
                vkn.append('00' + v)
            else:
                vkn.append(np.nan)
                tckn.append(np.nan)
        else:
            if(' ' in v):
                v = v.replace(' ', '')
            if(' ' in t):
                t = t.replace(' ', '')
            
            if(v == t):
                if(not v.isdecimal()):
                    tckn.append(t)
                    vkn.append(v)
                    continue
                if(len(v) == 11 and v[0] != '0'):
                    tckn.append(t)
                    vkn.append(np.nan)
                elif(len(v) == 10):
                    tckn.append(np.nan)
                    vkn.append(v)
                elif(len(v) == 9):
                    tckn.append(np.nan)
                    vkn.append('0' + v)
                elif(len(t) == 8):
                    tckn.append(np.nan)
                    vkn.append('00' + v)
                else:
                    vkn.append(np.nan)
                    tckn.append(np.nan)

            else:
                if(not t.isdecimal()):
                    tckn.append(np.nan)
                elif(len(t) == 11 and t[0] != '0'):
                    tckn.append(t)
                else:
                    tckn.append(np.nan)
            
                if(not v.isdecimal()):
                    vkn.append(np.nan)
                elif(len(v) == 10):
                    vkn.append(v)
                elif(len(v) == 9):
                    vkn.append('0' + v)
                elif(len(v) == 8):
                    vkn.append('00' + v)
                else:
                    vkn.append(np.nan)
                    
    return tckn, vkn

def check_tckn(t):
    if(pd.isna(t)):
        return np.nan
    t = str(t)
    if(' ' in t):
        t = t.replace(' ', '')
    if(len(t) != 11):
        return np.nan
    if(t[0] == '0'):
        return np.nan
    if(not t.isdecimal()):
        return np.nan
    else:
        return t

def check_vkn(v):
    if(pd.isna(v)):
        return np.nan
    v = str(v)
    if(' ' in v):
        v = v.replace(' ', '')
    if(not (len(v) == 10 or len(v) == 9 or len(v) == 8)):
        return np.nan
    if(not v.isdecimal()):
        return np.nan
    if(len(v) == 10):
        return v
    if(len(v) == 9):
        return '0' + v
    if(len(v) == 8):
        return '00' + v
    else:
        return v
    
def separate_tckn_vkn(col):
# takes a column of a df
# returns lists tckn&vkn

    tckn = []
    vkn = []
    
    for c in col:
        if(not pd.isna(check_tckn(c))):
            tckn.append(c)
            vkn.append(np.nan)
        elif(not pd.isna(check_vkn(c))):
            tckn.append(np.nan)
            vkn.append(c)
        else:
            tckn.append(np.nan),
            vkn.append(np.nan)
    return tckn, vkn


def transpose_memzuc_bySorguNo(df:pd.DataFrame):
    # pivot the data
    
    df['sorgu_no'] = df['sorgu_no'].astype(float).astype(int)
    df_melt = pd.melt(df,
                      id_vars=['donem_risk', 'sorgu_no'],
                      value_vars=['LIMIT','risk_0_12','risk_12_24',
                                  'risk_24','toplam_risk','faiz_tahakkuk',
                                  'reeskont','limit_adet','risk_adet'])
    df_melt['donem_r'] = df_melt['donem_risk'] + '_' + df_melt['variable']

    df_pivot = pd.pivot_table(df_melt, values = 'value',
                               aggfunc='first',
                               index=['sorgu_no'],
                               columns ='donem_r')

    df_pivot.reset_index(inplace=True)
    df_pivot.rename_axis(None, axis=1, inplace=True)
    df_pivot['sorgu_no'] = df_pivot['sorgu_no'].astype(str)
 
    return df_pivot

    
def correct_data(df):
    
    print('Correcting data in %s ... '%df.name, end=' ')
    if(df.name == 'master'):
        df.name = 'master'

    if(df.name == 'cek_risk'):
        df.name = 'cek_risk'
    
    if(df.name == 'memzuc'):
    
        df = transpose_memzuc_bySorguNo(df)
        
        df.name = 'memzuc'
    
    if(df.name == 'mersis_firma'):

        df['tckn'], df['vkn'] = separate_tckn_vkn(df['vergino'])
        df.drop(columns=['vergino'], inplace=True)

        if (df['tckn'].notna().sum() == 0):
            df.drop(columns=['tckn'], inplace=True)
        if (df['vkn'].notna().sum() == 0):
            df.drop(columns=['vkn'], inplace=True) 
        df.name = 'mersis_firma'

    if(df.name == 'mersis_ortak'):

        df['tckn'], df['vkn'] = check_2cols_tcvkn(df['tckimliknomtkno'],
                                                          df['vergino'])
        df.drop(columns=['tckimliknomtkno', 'vergino'], inplace=True)

        if (df['tckn'].notna().sum() == 0):
            df.drop(columns=['tckn'], inplace=True)
        if (df['vkn'].notna().sum() == 0):
            df.drop(columns=['vkn'], inplace=True)  
        df.name = 'mersis_ortak'

    if(df.name == 'mersis_nace'):

        df.name = 'mersis_nace'

    if(df.name == 'mersis_sermaye'):

        df['tckn'], df['vkn'] = check_2cols_tcvkn(df['tckimlikno'], 
                                                  df['vergino'])
        df.drop(columns=['tckimlikno', 'vergino'], inplace=True)

        if (df['tckn'].notna().sum() == 0):
            df.drop(columns=['tckn'], inplace=True)
        if (df['vkn'].notna().sum() == 0):
            df.drop(columns=['vkn'], inplace=True)  
        df.name = 'mersis_sermaye'

    if(df.name == 'mersis_temsilci'):

        df['tckn'], df['vkn'] = separate_tckn_vkn(df['tckimlikno'])
        df['adina_hareket_eden_tckn'], df['adina_hareket_eden_vkn'] = separate_tckn_vkn(df['adinahareketedenkisikimlikno'])
                
        df.name = 'mersis_temsilci'
    
    print('done!')
    return df
    


