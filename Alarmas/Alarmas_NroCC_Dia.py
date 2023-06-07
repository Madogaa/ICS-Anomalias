#%%

import os
os.chdir(r'C:\\Users\\mario\\OneDrive\\Documentos\\ICS Anomalías\\Códigos_Análisis')

import pandas as pd
from Datos.Base_datos import*
from Modelos_Alarmas.Modelo_NroCC_Dia import *
from Modelos_Alarmas.Modelo_NroCC import*

def alarmas_nrocc_dia(mes,dia):
    all = FiltroFinal()
    # 23-05-2023
    MESI_MAX = mes # Mes actual para comparar (contexto de datos)
    DIA_MAX= dia # Dia actual para comparar (contexto de datos)

    proyecto=[]
    emptydia=[]

    all = all[((all['mesi'] == MESI_MAX) & (all['diai'] <= DIA_MAX))]
    all = all[all['NroCC_Obra'].notna() & all['NroCC_Obra'].str.startswith('1')]
    nrocc= all['NroCC_Obra'].unique()
    mod = modelo_nrocc()
    prom = modelo_nrocc_dia()

    dias = round(all.groupby(['NroCC_Obra','diai']).MONTO.sum().to_frame()/1000000,3).reset_index()
    for id in nrocc:
        for dia in range(1, DIA_MAX+1):
            input = dias[(dias['NroCC_Obra'] == id) & (dias['diai'] == dia)]
            if input.empty :
                proyecto.append(id)
                emptydia.append(dia)

    diccionario = {'NroCC_Obra': proyecto,'diai': emptydia,'Monto': 0}
    empty = pd.DataFrame(diccionario)
    dias = pd.concat([dias,empty],axis=0).groupby(['NroCC_Obra','diai']).MONTO.sum().to_frame().reset_index()

    dias = dias.merge(mod,on=['NroCC_Obra'],how='inner')
    dias['VtaMes'] = dias['a'] * MESI_MAX**2 + dias['b'] * MESI_MAX + dias['c']
    dias = dias.drop(['a','b','c'],axis=1)
    dias['Gasto Real'] = dias.groupby(['NroCC_Obra'])['MONTO'].cumsum()
    dias['Gasto Real %'] = (dias['Gasto Real'] / dias['VtaMes'])  * 100
    dias = dias.merge(prom,on=['NroCC_Obra','diai'],how='inner')
    dias.loc[dias['Gasto Real %'] > (dias['nivel']), 'alarma'] = 'Gasto adelantado'
    dias['Gasto Prevista'] = (dias['prom'] / 100) * dias['VtaMes']
    dias = dias.rename(columns={'prom':'Gasto Prevista %','nivel': 'nivel %'})
    dias['nivel'] = (dias['nivel %'] / 100) * dias['VtaMes']
    datos = all[all['NroCC_Obra'].isin(dias['NroCC_Obra'].unique())]
    datos = datos[['NroCC_Obra','NombreCC_Obra']].drop_duplicates()
    dias = dias.merge(datos,on=['NroCC_Obra'],how='inner')
    dias = dias[['NroCC_Obra','NombreCC_Obra','diai','Gasto Real','Gasto Prevista','nivel','Gasto Real %','Gasto Prevista %','nivel %','alarma']]
    return dias

df = alarmas_nrocc_dia(29,31)
df = df[df['alarma'].notna()]
df.to_excel('Alarmas_NroCC_Dia.xlsx')
df
# %%
