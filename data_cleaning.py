import numpy as np

def clean_nans(df):
    df.replace(['None'], [np.nan], inplace=True)
    return df
    
def clean_data(df):
    
    print('Cleaning data in %s ... '%df.name, end=' ')
    if(df.name == 'master'):
        df = clean_nans(df)
        df.name = 'master'

    if(df.name == 'cek_risk'):
        df = clean_nans(df)
        df.name = 'cek_risk'

    if(df.name == 'memzuc'):
        df = clean_nans(df)
        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        df.fillna(0, inplace=True)
        df.name = 'memzuc'

    if(df.name == 'mersis_firma'):
        df = clean_nans(df)
        df.name = 'mersis_firma'
        
    if(df.name == 'mersis_ortak'):
        df = clean_nans(df)
        df.name = 'mersis_ortak'
        
    if(df.name == 'mersis_nace'):
        df = clean_nans(df)
        df.name = 'mersis_nace'
        
    if(df.name == 'mersis_sermaye'):
        df = clean_nans(df)
        df.name = 'mersis_sermaye'
        
    if(df.name == 'mersis_temsilci'):
        df = clean_nans(df)
        df.name = 'mersis_temsilci'
    
    if(df.name == 'all'):
        
        df.name = 'all'
        
    print('done!')
    return df

