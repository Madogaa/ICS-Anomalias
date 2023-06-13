# %%

import pandas as pd
from Datos.Base_datos import *
from Modelos_Alarmas.Modelo_Proy_Mes_Cuad import *

def alarmasventas(mes):
    MES = mes
    all=Filtro()
    all = all[(all['mesi'] == MES) & (all['TipoMov'] == 'VTA')]
    all = round(all.groupby(['IdProy','mesi']).Monto.sum().to_frame()/1000000,3).reset_index()
    pred = promventas()
    all = all.merge(pred,on=['IdProy'],how='inner')
    all['prom'] = (all['a'] * all['mesi']**2 + all['b'] * all['mesi'] + all['c'])
    all['nivel+'] =  all['prom'] + 1.28 * all['desv']
    all['nivel-'] =  all['prom'] - 1.28 * all['desv']
    all.loc[(all['Monto'] < all['nivel-']), 'alarma'] = 'Ventas bajas'
    all.loc[(all['Monto'] > all['nivel+']), 'alarma'] = 'Ventas altas'
    all = all[~all['alarma'].isnull()]
    all = all.drop(['a','b','c','desv'],axis=1)
    return all

def alarmasventas_rango(mesi,mesf):
    all=Filtro()
    all = all[(all['mesi'] >= mesi) & (all['mesi'] <= mesf) & (all['TipoMov'] == 'VTA')]
    all = round(all.groupby(['IdProy','mesi']).Monto.sum().to_frame()/1000000,3).reset_index()
    pred = promventas()
    all = all.merge(pred,on=['IdProy'],how='inner')
    all['prom'] = (all['a'] * all['mesi']**2 + all['b'] * all['mesi'] + all['c'])
    all['nivel+'] =  all['prom'] + 1.28 * all['desv']
    all['nivel-'] =  all['prom'] - 1.28 * all['desv']
    all.loc[(all['Monto'] < all['nivel-']), 'alarma'] = 'Ventas bajas'
    all.loc[(all['Monto'] > all['nivel+']), 'alarma'] = 'Ventas altas'
    all = all[~all['alarma'].isnull()]
    all = all.drop(['a','b','c','desv'],axis=1)
    return all


def alarmasgastos(mes):
    MES = mes
    all=Filtro()
    all = all[(all['mes'] == MES) & ((all['TipoMov'] == 'GTO') | (all['TipoMov'] == 'ACT'))]
    all = round(all.groupby(['IdProy','mes']).Monto.sum().to_frame()/1000000,3).reset_index()
    pred = promgastos()
    all = all.merge(pred,on=['IdProy'],how='inner')
    all['prom'] = (all['a'] * all['mes']**2 + all['b'] * all['mes'] + all['c'])
    all['nivel+'] =  all['prom'] + 1.28 * all['desv']
    all['nivel-'] =  all['prom'] - 1.28 * all['desv']
    all.loc[(all['Monto'] < all['nivel-']), 'alarma'] = 'Gastos altos'
    all.loc[(all['Monto'] > all['nivel+']), 'alarma'] = 'Gastos bajos'
    all = all[~all['alarma'].isnull()]
    all = all.drop(['a','b','c','desv'],axis=1)
    return all

def alarmasmb(mes):
    MES = mes
    all = Filtro()
    all = all[(all['mesi'] == MES)]
    all = round(all.groupby(['IdProy','mesi']).Monto.sum().to_frame()/1000000,3).reset_index()
    pred = prommb()
    all = all.merge(pred,on=['IdProy'],how='inner')
    all['prom'] = (all['a'] * all['mesi']**2 + all['b'] * all['mesi'] + all['c'])
    all['nivel+'] =  all['prom'] + 1.28 * all['desv']
    all['nivel-'] =  all['prom'] - 1.28 * all['desv']
    all.loc[(all['Monto'] < all['nivel-']), 'alarma'] = 'MB bajo'
    all.loc[(all['Monto'] > all['nivel+']), 'alarma'] = 'MB alto'
    all = all[~all['alarma'].isnull()]
    all = all.drop(['a','b','c','desv'],axis=1)
    return all

df = alarmasmb(29)
df
# %%
