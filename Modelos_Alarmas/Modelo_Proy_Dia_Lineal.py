# %%
import os
os.chdir(r'C:\\Users\\mario\\Downloads\\AnalisisICS-Test\\Modelo')

import pandas as pd
import itertools
from Datos.Base_datos import *
from Modelo_Proy_Mes_Cuad import *

def promdiafact():
    all = Filtro()
    all = all[((all['mesi'] < 29)) & (all['TipoMov'] == 'VTA') & (all['Monto']>=0)]
    ##
    MESI_RNG = range(1, 29)
    DIAS_RNG = range(1, 32)
    NIVEL = 1.28 # 80% De los casos
    ##
    vtaxmes = round(all.groupby(['IdProy','mesi']).Monto.sum().to_frame()/1000000,3)
    vtaxmes = vtaxmes.rename(columns={'Monto':'VTAxMes'})
    vtaxmes = vtaxmes.reset_index()
    ##
    vtaxdia = round(all.groupby(['IdProy','mesi','diai']).Monto.sum().to_frame()/1000000,3)
    vtaxdia = vtaxdia.rename(columns={'Monto':'VTAxDia'})
    vtaxdia = vtaxdia.reset_index()
    ##
    idproy = vtaxdia['IdProy'].unique()
    ##
    all_combinations = pd.DataFrame(list(itertools.product(idproy,MESI_RNG,DIAS_RNG)),columns=['IdProy', 'mesi', 'diai'])
    all_combinations['VTAxDia'] = 0
    merged = pd.merge(all_combinations, vtaxdia, how='outer', on=['IdProy', 'mesi', 'diai'])
    merged['VTAxDia_y'] = merged['VTAxDia_y'].fillna(0)
    merged = merged.drop(['VTAxDia_x'],axis=1)
    merged = merged.rename(columns={'VTAxDia_y':'VTAxDia'})
    ##
    vtaxdia = merged
    vtaxdiap = vtaxdia.merge(vtaxmes,on=['IdProy','mesi'],how='inner')
    vtaxdiap['Monto%'] = round((vtaxdiap['VTAxDia'] / vtaxdiap['VTAxMes']) * 100,1)
    vtaxdiap['Monto'] = vtaxdiap.groupby(['IdProy','mesi'])['Monto%'].cumsum()
    vtaxdiap = vtaxdiap.dropna(subset=['Monto'])
    ##
    promedio = vtaxdiap.groupby(['IdProy','diai'])['Monto'].mean().to_frame()
    promedio = promedio.rename(columns={'Monto':'prom'})
    promedio = promedio.reset_index()
    ##
    desv = vtaxdiap.groupby(['IdProy','diai'])['Monto'].std().to_frame()
    desv = desv.rename(columns={'Monto':'desv'})
    desv = desv.reset_index()
    desv = desv.fillna(0)
    ##
    promedio = promedio.merge(desv,on=['IdProy','diai'],how='inner')
    promedio['nivel'] = promedio['prom'] - NIVEL * promedio['desv']
    promedio.loc[promedio['nivel'] < 0 , 'nivel'] = 0
    return promedio

def promdiagto():
    all = Filtro()
    all = all[((all['mesi'] < 29)) & ((all['TipoMov'] == 'GTO') | (all['TipoMov'] == 'ACT') ) & (all['Monto']<=0)]
    ##
    MESI_RNG = range(1, 29)
    DIAS_RNG = range(1, 32)
    NIVEL = 1.28 # 80% De los casos
    ##
    vtaxmes = round(all.groupby(['IdProy','mesi']).Monto.sum().to_frame()/1000000,3)
    vtaxmes = vtaxmes.rename(columns={'Monto':'VTAxMes'})
    vtaxmes = vtaxmes.reset_index()
    ##
    vtaxdia = round(all.groupby(['IdProy','mesi','diai']).Monto.sum().to_frame()/1000000,3)
    vtaxdia = vtaxdia.rename(columns={'Monto':'VTAxDia'})
    vtaxdia = vtaxdia.reset_index()
    ##
    idproy = vtaxdia['IdProy'].unique()
    ##
    all_combinations = pd.DataFrame(list(itertools.product(idproy,MESI_RNG,DIAS_RNG)),columns=['IdProy', 'mesi', 'diai'])
    all_combinations['VTAxDia'] = 0
    merged = pd.merge(all_combinations, vtaxdia, how='outer', on=['IdProy', 'mesi', 'diai'])
    merged['VTAxDia_y'] = merged['VTAxDia_y'].fillna(0)
    merged = merged.drop(['VTAxDia_x'],axis=1)
    merged = merged.rename(columns={'VTAxDia_y':'VTAxDia'})
    ##
    vtaxdia = merged
    vtaxdiap = vtaxdia.merge(vtaxmes,on=['IdProy','mesi'],how='inner')
    vtaxdiap['Monto%'] = round((vtaxdiap['VTAxDia'] / vtaxdiap['VTAxMes']) * 100,1)
    vtaxdiap['Monto'] = vtaxdiap.groupby(['IdProy','mesi'])['Monto%'].cumsum()
    vtaxdiap = vtaxdiap.dropna(subset=['Monto'])
    ##
    promedio = vtaxdiap.groupby(['IdProy','diai'])['Monto'].mean().to_frame()
    promedio = promedio.rename(columns={'Monto':'prom'})
    promedio = promedio.reset_index()
    ##
    desv = vtaxdiap.groupby(['IdProy','diai'])['Monto'].std().to_frame()
    desv = desv.rename(columns={'Monto':'desv'})
    desv = desv.reset_index()
    desv = desv.fillna(0)
    ##
    promedio = promedio.merge(desv,on=['IdProy','diai'],how='inner')
    promedio['nivel'] = promedio['prom'] + NIVEL * promedio['desv']
    promedio.loc[promedio['nivel'] < 0 , 'nivel'] = 0
    return promedio
