# constants, lists, dictionaries, paths that are used
import pandas as pd

# PATHS:
path_envanter = '../Docs/veri_envanteri.xlsx'

path_data_in_csv = '../Data/merged_data.csv'
path_data_w_prod_features = '../Data/features.csv'

# envanter
envanter = pd.read_excel(path_envanter,
                         sheet_name='veri_envanteri')

# data types dictionary
type_conversion = {'id':str,
                   'date':'date',
                   'integer':pd.Int64Dtype(),
                   'float':float,
                   'string':str,
                   'categorical':str,
                   'boolean':int}

db_names = {'':''}

# model_name:(model_path, features, target)
model = {'model1':{'path':'../Model/XGB_model1',
                   'features':envanter[envanter['model'] == 1]['veri'],
                   'target':'karsiliksiz'}}


