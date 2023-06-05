# %%
import os
os.chdir(r'C:\\Users\\mario\\OneDrive\\Documentos\\ICS Anomalías\\Códigos_Análisis')

import pandas as pd
from Modelos_Alarmas.Modelo_NroCuenta import *

def alarmas_nrocue(mes):
    MES = mes
    all = Filtro()
    all = all[(all['mesi'] == MES)]
    lista=['IdProy','CuentaNro','CuentaNombre','mesi']

    mod = modelo_nrocue()

    NrosCuenta = ['4110101','4210213','4210103','4210211','4210101','4210212','4210501']
    NrosCuentaT = ['4110101','4210213','4210103','4210211','4210101','4210212','4210501','1000000']
    all['CuentaNombre'] = all['CuentaNombre'].str.strip()

    nrocu = round(all.groupby(by=lista).Monto.sum().to_frame()/1000000,3).reset_index()
    nrocu.loc[~nrocu['CuentaNro'].isin(NrosCuenta),'CuentaNombre']='VARIOS'
    nrocu.loc[~nrocu['CuentaNro'].isin(NrosCuenta),'CuentaNro']='1000000'
    nrocu = (nrocu.groupby(lista).Monto.sum().to_frame()).reset_index()
    nrocu = nrocu.merge(mod,on=['IdProy','CuentaNro'],how='inner')
    nrocu['nivel+'] = ((nrocu['a'] * nrocu['mesi']**2) + nrocu['b'] * nrocu['mesi'] + nrocu['c']) + 1.28* nrocu['desv']
    nrocu['nivel-'] = ((nrocu['a'] * nrocu['mesi']**2) + nrocu['b'] * nrocu['mesi'] + nrocu['c']) - 1.28* nrocu['desv']
    nrocu.loc[nrocu['Monto']>nrocu['nivel+'],'alarma'] = 'NroCuenta bajo'
    nrocu.loc[nrocu['Monto']<nrocu['nivel-'],'alarma'] = 'NroCuenta alto'
    nrocu = nrocu.drop(['a','b','c','desv'],axis=1)
    nrocu = nrocu[~(nrocu['CuentaNro'] == '4110101')]
    nrocu = nrocu[~nrocu['alarma'].isnull()]
    return nrocu

df = alarmas_nrocue(29)
df.to_excel('nrocuenta.xlsx')
df
# %%
