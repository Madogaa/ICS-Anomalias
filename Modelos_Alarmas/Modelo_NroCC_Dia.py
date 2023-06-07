# %%

import os
os.chdir(r'C:\\Users\\mario\\OneDrive\\Documentos\\ICS Anomalías\\Códigos_Análisis')

import pandas as pd
import itertools
from Datos.Base_datos import*

def modelo_nrocc_dia():
    MES_MAX = 29
    all = FiltroFinal()
    all = all[((all['mesi'] < MES_MAX))]
    all = all[all['NroCC_Obra'].notna() & all['NroCC_Obra'].str.startswith('1')]
    ##
    MESI_RNG = range(1, MES_MAX)
    DIAS_RNG = range(1, 32)
    NIVEL = 1.28 # 80% De los casos
    ##
    vtaxmes = round(all.groupby(['NroCC_Obra','mesi']).MONTO.sum().to_frame()/1000000,3)
    vtaxmes = vtaxmes.rename(columns={'MONTO':'MontoxMes'}).reset_index()
    ##
    vtaxdia = round(all.groupby(['NroCC_Obra','mesi','diai']).MONTO.sum().to_frame()/1000000,3).reset_index()
    ##
    nrocc = vtaxdia['NroCC_Obra'].unique()
    ##
    all_combinations = pd.DataFrame(list(itertools.product(nrocc,MESI_RNG,DIAS_RNG)),columns=['NroCC_Obra', 'mesi', 'diai'])
    merged = pd.merge(all_combinations, vtaxdia, how='outer', on=['NroCC_Obra', 'mesi', 'diai'])
    merged['MONTO'] = merged['MONTO'].fillna(0)
    ##
    merged = merged.merge(vtaxmes,on=['NroCC_Obra','mesi'],how='inner')
    merged['Monto%'] = round((merged['MONTO'] / merged['MontoxMes']) * 100,1)
    merged['MontoA'] = merged.groupby(['NroCC_Obra','mesi'])['Monto%'].cumsum()
    merged = merged.dropna(subset=['MontoA'])
    ##
    merged = merged.drop(['MONTO','Monto%'],axis=1)
    ##
    promedio = merged.groupby(['NroCC_Obra','diai'])['MontoA'].mean().to_frame()
    promedio = promedio.rename(columns={'MontoA':'prom'}).reset_index()
    #
    desv = merged.groupby(['NroCC_Obra','diai'])['MontoA'].std().to_frame()
    desv = desv.rename(columns={'MontoA':'desv'}).reset_index().fillna(0)
    promedio = promedio.merge(desv,on=['NroCC_Obra','diai'],how='inner')
    promedio['nivel'] = promedio['prom'] + NIVEL * promedio['desv']
    promedio.loc[promedio['nivel'] < 0 , 'nivel'] = 0
    ##
    return promedio

df = modelo_nrocc_dia()
df
# %%



