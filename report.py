import pandas as pd
from xgboost.sklearn import XGBClassifier
from sklearn.metrics import roc_auc_score
import pickle
import lookup

def prepare_report(df_test, model, target='karsiliksiz'):
    X = df_test.drop(columns=[target])
    y = df_test[target]

    predprobs = model.predict_proba(X)[:,1]
    preds = model.predict(X)
    
    df['predprob'] = predprobs
    df['real'] = y
    df['pred'] = preds

    def score(x):
        
        if x > 0.813:
            group = 'F'
        elif x > 0.632:
            group = 'E'
        elif x > 0.493:
            group = 'D'
        elif x > 0.295:
            group = 'C'
        elif x > 0.1685: 
            group = 'B'
        else:
            group = 'A'
            
    return group


    df['score'] = df['predprobs'].apply(lambda x: score(x))

    df_report = pd.DataFrame()

    df_report['Grup'] = ['F', 'E', 'D', 'B', 'A']

    dfa = df[df['score'] == 'A'] 
    dfb = df[df['score'] == 'B']
    dfc = df[df['score'] == 'C']
    dfd = df[df['score'] == 'D']
    dfe = df[df['score'] == 'E']
    dff = df[df['score'] == 'F']

    groups = [dff, dfe, dfd, dfc, dfb, dfa]

    
    cek_sayisi = []
    kar_cek_sayisi = []
    populasyon = []
    kar_yakalama_orani = []
    grup_kar_adet = []
    tutar = []
    grup_kar_tutar = []
    
    for g in groups:
        # ÇEK SAYISI
        cek_sayisi.append(len(g))
        # KARŞILIKSIZ ÇEK SAYISI
        kar_cek_sayisi.append(len(g[g['real'] == 1]))
        # POPÜLASYON
        populasyon.append(round(len(g)/len(df_test)*100, 1))
        # KARSILIKSIZI YAKALAMA ORANI
        if(len(g[g['real'] == 1]) == 0):
            kar_yakalama_orani.append('NA')
        else:
            kar_yakalama_orani.append(round(len(g[g['real'] == 1]\
                                      [g['pred'] == 1])/\
                                  len(g[g['real'] == 1])*100, 2))

        # GRUPTAKİ KARŞILIKSIZI %(ADET)
        if(len(g) == 0):
            grup_kar_adet.append('NA')
        else:
            grup_kar_adet.append(round(len(g[g['real'] == 1])/len(g)*100, 2))
        # TUTAR 
        tutar.append(g['tutar'].sum())
        # GRUPTAKİ KARŞILIKSIZ %(TUTAR)
        if(g['tutar'].sum() == 0):
            grup_kar_tutar.append('NA')
        else:
            grup_kar_tutar.append(round(g[g['real'] == 1]['tutar'].sum()\
                              /g['tutar'].sum()*100, 2))

    df_report['Çek Sayısı'] = cek_sayisi
    df_report['Karşılıksız Çek Sayısı'] = kar_cek_sayisi
    df_report['Popülasyon %'] = populasyon
    df_report['Karşılıksızı Yakalama Oranı'] = kar_yakalama_orani
    df_report['Gruptaki Karşılıksız % (Adet)'] = grup_kar_adet
    df_report['Toplam Tutar'] = tutar
    df_report['Gruptaki Karşılıksız % (Tutar)'] = grup_kar_tutar

    df_report.to_csv('../Prediction/Model_raporu.csv', index=False)
