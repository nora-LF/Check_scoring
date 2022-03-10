import time
start_time = time.time()
print('Training started.')

from data_retrieval import *
from data_correction import *
from data_creation import *
from data_prep import *
import pandas as pd
import psycopg2
import lookup
from sklearn.model_selection import train_test_split
from xgboost.sklearn import XGBClassifier
from sklearn.metrics import roc_auc_score

# veri envanteri
envanter = pd.read_excel(lookup.path_envanter,
                         sheet_name='veri_envanteri')

# read from postgre or csv
data_source = 'csv'

if(data_source == 'postgre'):
    df = prepare_data(['tableA', 'tableB', 'tableC'])
    
if(data_source == 'csv'):
    df = retrieve_data(data_source='csv')

prod_features = list(pd.read_excel(lookup.path_envanter,
                         sheet_name='prod_features')['yeni_ismi'])
prod_features.append('karsiliksiz')

df = df.reset_index().drop_duplicates(subset=['islem_tar', 
                                              'islem_ref', 
                                              'line_no'],
                                      keep='last').set_index('index')
# tutar
df = df[df['tutar'] >= 2000]
df = df[df['tutar'] <= 500000]
# vade
df = df[df['gun'] >= 3]
df = df[df['gun'] <= 365]

fark_date_cols = ['fark_ibraz_ilk',
                  'fark_ibraz',
                  'fark_eneski',
                  'fark_ilk'
                  'fark_son_kar',
                  'fark_enguncellimit',
                  'fark_ilkkredim',
                  'fark_sonkredi',
                  'fark_skitakip',
                  'fark_takip']

for c in fark_date_cols:
    if(c in df.columns):
        df = df[df[c] > 0]
for c in fark_date_cols:
    if(c in df.columns):
        df[c] = np.where(df[c] >= 7300, 99999, df[c])

df = df[prod_features]
X = df.drop(columns=['karsiliksiz'])
y = df['karsiliksiz']

X_train, X_test, y_train, y_test = train_test_split(X, 
                                                    y, 
                                                    test_size=0.80, 
                                                    random_state=42)
sum_ps = sum(y_train)
sum_ng = len(y_train) - sum(y_train)
pos_wgt = round(sum_ng/sum_ps,2)

XGBoostParam = {"n_estimators" : 250, 
                "max_depth" : 5, 
                'learning_rate' : 0.01, 
                "min_child_weight": 1, 
                'seed': 123, 
                'verbose': True, 
                'scale_pos_weight': pos_wgt, 
                'eval_metric': 'auc'}

clf= XGBClassifier(**XGBoostParam)
clf.fit(X_train, y_train)
preds = clf.predict_proba(X_test)[:,1]
auc = roc_auc_score(y_test,preds)
print('test accuracy: ', auc)

df_test = pd.concat([X_test, y_test], axis=1)

prepare_report(df_test, clf)

end_time = time.time()
print('Training ended. Duration: %d'%(end_time - start_time))
