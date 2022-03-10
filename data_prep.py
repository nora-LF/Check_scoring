'''
1. data_retrieval.py
2. data_correction.py
3. data_cleaning.py
4. data_merge.py
5. data_creation.py
6. data_prep.py
7. model_training.py
'''

from data_retrieval import *
from data_correction import *
from data_creation import *
from data_cleaning import *

def prepare_data(datanames):

    if('tableA' in datanames):
        tableA = retrieve_data('tableA')
        tableA = correct_data(tableA)
        tableA = clean_data(tableA)
        tableA = create_data(tableA)
        
    if('tableB' in datanames):
        tableB = retrieve_data('tableB')
        tableB = correct_data(tableB)
        tableB = clean_data(tableB)
        tableB = create_data(tableB)
    
        # master & cek_risk
        print('Merging tableA and tableB data ... ', end=' ')
        
        df = tableA.merge(tableB,
                       how='left',
                       left_on=['c_sorgu', 'r_sorgu'],
                       right_on=['1sorgu_no', '2sorgu_no'])
        
        print('done!')
        
    if('tableC' in datanames):
    
        tableC = retrieve_data('tableC')
        tableC = correct_data(tableC)
        tableC = create_data(tableC)
        tableC = clean_data(tableC)

        print('Adding tableC data ... ', end=' ')
        
        df = df.merge(tableC, 
                      how='left',
                      left_on='kes_m_sorgu',
                      right_on='sorgu_no')
        
        print('done!')

       
    df.name = 'all'
    df = create_data(df)
    df = clean_data(df)

    df.name = 'all'
    return df
