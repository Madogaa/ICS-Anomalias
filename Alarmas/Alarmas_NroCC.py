# %%

import os
os.chdir(r'C:\\Users\\mario\\OneDrive\\Documentos\\ICS Anomalías\\Códigos_Análisis')

from Datos.Base_datos import*
from Modelos_Alarmas.Modelo_NroCC import*
import pandas as pd

def alarmas_nrocue(mes):
    MES = mes
    all = FiltroFinal()
    all = all[(all['mesi'] == MES)]
    lista = ['NroCC_Obra', 'NombreCC_Obra', 'mesi']

    mod = modelo_nrocc()
    nrocu = round(all.groupby(by=lista).MONTO.sum().to_frame() / 1000000, 3).reset_index()
    nrocu = nrocu[nrocu['NroCC_Obra'].str.startswith('1')]
    nrocu = nrocu.merge(mod,on=['NroCC_Obra'],how='inner')
    nrocu['nivel+'] = ((nrocu['a'] * nrocu['mesi']**2) + nrocu['b'] * nrocu['mesi'] + nrocu['c']) + 1.28* nrocu['desv']
    nrocu['nivel-'] = ((nrocu['a'] * nrocu['mesi']**2) + nrocu['b'] * nrocu['mesi'] + nrocu['c']) - 1.28* nrocu['desv']
    nrocu.loc[nrocu['MONTO']>nrocu['nivel+'],'alarma'] = 'NroCC bajo'
    nrocu.loc[nrocu['MONTO']<nrocu['nivel-'],'alarma'] = 'NroCC alto'
    nrocu = nrocu.drop(['a','b','c','desv'],axis=1)
    nrocu = nrocu[~nrocu['alarma'].isnull()]
    return nrocu

df = alarmas_nrocue(29)
df

# %%
