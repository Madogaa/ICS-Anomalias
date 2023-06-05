import pandas as pd
from Modelo_Proy_Mes_Cuad import *

mod = promedioventas()
criterio1 = mod[['IdProy','m_proy_vta','b_proy_vta','desv_proy_vta']].drop_duplicates()
criterio1 = criterio1.dropna(subset=['m_proy_vta','b_proy_vta','desv_proy_vta'], how='all')

all = pd.read_feather(datos)
all = all[((all['mesi'] > 24) & (all['mesi'] < 29)) & (all['TipoMov'] == 'VTA')]

lista = ['IdProy','mesi']
# all = all[all['Monto']>=0]

vtaxmes = round(all.groupby(lista).Monto.sum().to_frame()/1000000,3)
vtaxmes = vtaxmes.rename(columns={'Monto':'VTAxMes'})
vtaxmes = vtaxmes.reset_index()
vtaxmes['VtaAcum'] = vtaxmes.groupby(['IdProy'])['VTAxMes'].cumsum()
vtaxmes = vtaxmes.drop(['VTAxMes'],axis=1)
vtaxmes = vtaxmes.merge(criterio1,on=['IdProy'],how='inner')
vtaxmes['montomod'] = vtaxmes['m_proy_vta'] * vtaxmes['mesi'] + vtaxmes['b_proy_vta']
vtaxmes['VtaAcumMod'] = vtaxmes.groupby(['IdProy'])['montomod'].cumsum()
vtaxmes= vtaxmes.drop(['m_proy_vta','b_proy_vta','desv_proy_vta','montomod'],axis=1)
vtaxmes.loc[vtaxmes['VtaAcum']< (vtaxmes['VtaAcumMod'] * 0.8) ,'alarma']= 'VentaAcum baja'
vtaxmes.loc[vtaxmes['VtaAcum']> (vtaxmes['VtaAcumMod'] * 1.2) ,'alarma']= 'VentaAcum alta'
vtaxmes = vtaxmes[vtaxmes['alarma'].notnull()]
vtaxmes = vtaxmes.reset_index()
vtaxmes.to_feather(rprueba + 'first.fth')
vtaxmes