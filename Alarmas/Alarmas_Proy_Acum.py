
# %%
import os
os.chdir(r'C:\\Users\\mario\\OneDrive\\Documentos\\ICS Anomalías\\Códigos_Análisis')

import pandas as pd
from Modelos_Alarmas.Modelo_Proy_Mes_Cuad import *

def alarmasventas_acum():
    mod = promventas()

    all = Filtro()
    all = all[((all['mesi'] > 24) & (all['mesi'] < 30)) & (all['TipoMov'] == 'VTA')]

    lista = ['IdProy','mesi']

    vtaxmes = round(all.groupby(lista).Monto.sum().to_frame()/1000000,3)
    vtaxmes = vtaxmes.rename(columns={'Monto':'VTAxMes'})
    vtaxmes = vtaxmes.reset_index()
    vtaxmes['VtaAcum'] = vtaxmes.groupby(['IdProy'])['VTAxMes'].cumsum()
    vtaxmes = vtaxmes.drop(['VTAxMes'],axis=1)
    vtaxmes = vtaxmes.merge(mod,on=['IdProy'],how='inner')
    vtaxmes['montomod'] = vtaxmes['a'] * vtaxmes['mesi']**2 + vtaxmes['b'] * vtaxmes['mesi'] + vtaxmes['c'] + 1.28
    vtaxmes['VtaAcumMod'] = vtaxmes.groupby(['IdProy'])['montomod'].cumsum()
    vtaxmes= vtaxmes.drop(['a','b','c','desv','montomod'],axis=1)
    vtaxmes.loc[vtaxmes['VtaAcum']< (vtaxmes['VtaAcumMod'] * 0.8) ,'alarma']= 'VentaAcum baja'
    vtaxmes.loc[vtaxmes['VtaAcum']> (vtaxmes['VtaAcumMod'] * 1.2) ,'alarma']= 'VentaAcum alta'
    vtaxmes = vtaxmes[vtaxmes['alarma'].notnull()]
    return vtaxmes

def alarmasgastos_acum():
    mod = promgastos()

    all = Filtro()
    all = all[((all['mes'] > 24) & (all['mes'] < 30)) & ((all['TipoMov'] == 'GTO')|(all['TipoMov'] == 'ACT'))]

    lista = ['IdProy','mes']

    gtoxmes = round(all.groupby(lista).Monto.sum().to_frame()/1000000,3)
    gtoxmes = gtoxmes.rename(columns={'Monto':'GTOxMes'})
    gtoxmes = gtoxmes.reset_index()
    gtoxmes['GtoAcum'] = gtoxmes.groupby(['IdProy'])['GTOxMes'].cumsum()
    gtoxmes = gtoxmes.drop(['GTOxMes'],axis=1)
    gtoxmes = gtoxmes.merge(mod,on=['IdProy'],how='inner')
    gtoxmes['montomod'] = gtoxmes['a'] * gtoxmes['mes']**2 + gtoxmes['b'] * gtoxmes['mes'] + gtoxmes['c'] + 1.28
    gtoxmes['GtoAcumMod'] = gtoxmes.groupby(['IdProy'])['montomod'].cumsum()
    gtoxmes= gtoxmes.drop(['a','b','c','desv','montomod'],axis=1)
    gtoxmes.loc[gtoxmes['GtoAcum']< (gtoxmes['GtoAcumMod'] * 0.8) ,'alarma']= 'GastoAcum alto'
    gtoxmes.loc[gtoxmes['GtoAcum']> (gtoxmes['GtoAcumMod'] * 1.2) ,'alarma']= 'GastoAcum bajo'
    gtoxmes = gtoxmes[gtoxmes['alarma'].notnull()]
    return gtoxmes

def alarmasmb_acum():
    mod = prommb()

    all = Filtro()
    all = all[((all['mesi'] > 24) & (all['mesi'] < 30))]

    lista = ['IdProy','mesi']

    mbxmes = round(all.groupby(lista).Monto.sum().to_frame()/1000000,3)
    mbxmes = mbxmes.rename(columns={'Monto':'mbxmes'})
    mbxmes = mbxmes.reset_index()
    mbxmes['MbAcum'] = mbxmes.groupby(['IdProy'])['mbxmes'].cumsum()
    mbxmes = mbxmes.drop(['mbxmes'],axis=1)
    mbxmes = mbxmes.merge(mod,on=['IdProy'],how='inner')
    mbxmes['montomod'] = mbxmes['a'] * mbxmes['mesi']**2 + mbxmes['b'] * mbxmes['mesi'] + mbxmes['c'] + 1.28
    mbxmes['MbAcumMod'] = mbxmes.groupby(['IdProy'])['montomod'].cumsum()
    mbxmes= mbxmes.drop(['a','b','c','desv','montomod'],axis=1)
    mbxmes.loc[mbxmes['MbAcum']< (mbxmes['MbAcumMod'] * 0.8) ,'alarma']= 'MBAcum bajo'
    mbxmes.loc[mbxmes['MbAcum']> (mbxmes['MbAcumMod'] * 1.2) ,'alarma']= 'MBAcum alto'
    mbxmes = mbxmes[mbxmes['alarma'].notnull()]
    return mbxmes

df = alarmasgastos_acum()
df

# %%
