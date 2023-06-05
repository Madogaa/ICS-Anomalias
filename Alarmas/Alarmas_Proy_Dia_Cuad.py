#%%
import os
os.chdir(r'C:\\Users\\mario\\OneDrive\\Documentos\\ICS Anomalías\\Códigos_Análisis')

import pandas as pd
from Datos.Base_datos import *
from Modelos_Alarmas.Modelo_Proy_Dia_Cuad import*

# Alarma de si algún día se ha podido retrasar alguna venta de lo previsto según el modelo
def alarmasdiavta(mes,dia):
    all = Filtro()
    # 23-05-2023
    MESI_MAX = mes # Mes actual para comparar (contexto de datos)
    DIA_MAX= dia # Dia actual para comparar (contexto de datos)

    proyecto=[]
    emptydia=[]

    all = all[((all['mesi'] == MESI_MAX) & (all['diai'] <= DIA_MAX)) & (all['TipoMov'] == 'VTA') & (all['Monto'] >= 0)]
    idproy= all['IdProy'].unique()
    mod = promventas()
    prom = promdiafact()

    dias = round(all.groupby(['IdProy','diai']).Monto.sum().to_frame()/1000000,3).reset_index()
    for id in idproy:
        for dia in range(1, DIA_MAX+1):
            input = dias[(dias['IdProy'] == id) & (dias['diai'] == dia)]
            if input.empty :
                proyecto.append(id)
                emptydia.append(dia)

    diccionario = {'IdProy': proyecto,'diai': emptydia,'Monto': 0}
    empty = pd.DataFrame(diccionario)
    dias = pd.concat([dias,empty],axis=0).groupby(['IdProy','diai']).Monto.sum().to_frame().reset_index()

    dias = dias.merge(mod,on=['IdProy'],how='inner')
    dias['VtaMes'] = dias['a'] * MESI_MAX**2 + dias['b'] * MESI_MAX + dias['c']
    dias = dias.drop(['a','b','c'],axis=1)
    dias['Venta Real'] = dias.groupby(['IdProy'])['Monto'].cumsum()
    dias['Venta Real %'] = (dias['Venta Real'] / dias['VtaMes'])  * 100
    dias = dias.merge(prom,on=['IdProy','diai'],how='inner')
    dias.loc[dias['Venta Real %'] < (dias['nivel']), 'alarma'] = 'Facturacion retrasada'
    dias['Venta Prevista'] = (dias['prom'] / 100) * dias['VtaMes']
    dias = dias.rename(columns={'prom':'Venta Prevista %','nivel': 'nivel %'})
    dias['nivel'] = (dias['nivel %'] / 100) * dias['VtaMes']
    dias = dias[['IdProy','diai','Venta Real','Venta Prevista','nivel','Venta Real %','Venta Prevista %','nivel %','alarma']]
    return dias

# Alarma de si algún día se ha facturado un gasto antes de lo previsto segun el modelo
def alarmasdiagto(mes,dia):
    all = Filtro()

    MESI_MAX = mes # Mes actual para comparar (contexto de datos)
    DIA_MAX= dia # Dia actual para comparar (contexto de datos)

    proyecto=[]
    emptydia=[]

    all = all[((all['mes'] == MESI_MAX) & (all['dia'] <= DIA_MAX)) & ((all['TipoMov'] == 'GTO') | (all['TipoMov'] == 'ACT')) & (all['Monto']<=0)]
    idproy= all['IdProy'].unique()
    mod = promgastos()
    prom = promdiagto()
    dias = round(all.groupby(['IdProy','dia']).Monto.sum().to_frame()/1000000,3).reset_index()
    for id in idproy:
        for dia in range(1, DIA_MAX+1):
            input = dias[(dias['IdProy'] == id) & (dias['dia'] == dia)]
            if input.empty :
                proyecto.append(id)
                emptydia.append(dia)
    diccionario = {'IdProy': proyecto,'dia': emptydia,'Monto': 0}
    empty = pd.DataFrame(diccionario)
    dias = pd.concat([dias,empty],axis=0).groupby(['IdProy','dia']).Monto.sum().to_frame().reset_index()

    dias = dias.merge(mod,on=['IdProy'],how='inner')
    dias['VtaMes'] = dias['a'] * MESI_MAX**2 + dias['b'] * MESI_MAX + dias['c']
    dias = dias.drop(['a','b','c'],axis=1)
    dias['Gasto Real'] = dias.groupby(['IdProy'])['Monto'].cumsum()
    dias['Gasto Real %'] = (dias['Gasto Real'] / dias['VtaMes'])  * 100
    dias = dias.merge(prom,on=['IdProy','dia'],how='inner')
    dias.loc[dias['Gasto Real %'] < (dias['nivel']), 'alarma'] = 'Facturacion retrasada'
    dias['Gasto Previsto'] = (dias['prom'] / 100) * dias['VtaMes']
    dias = dias.rename(columns={'prom':'Gasto Previsto %','nivel': 'nivel %'})
    dias['nivel'] = (dias['nivel %'] / 100) * dias['VtaMes']
    dias = dias[['IdProy','dia','Gasto Real','Gasto Previsto','nivel','Gasto Real %','Gasto Previsto %','nivel %','alarma']]
    return dias

df = alarmasdiagto(29,31)
# df = df[~df['alarma'].isnull() & (df['diai'] == 29)]
df
# %%
