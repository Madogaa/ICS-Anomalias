# %%

import pandas as pd
import feather as fd
import numpy as np
from datetime import datetime
ruta = 'C:/Users/AdministradorICS/Documents/'
ruta2 = 'C:/Users/AdministradorICS/Documents/ExcelBD'


mod = pd.read_feather(ruta+'ModeloProyGastos_BD.fth')

datos = pd.read_feather(ruta+'DatosBD.feather')
datos = datos[(datos['mesi'] == 28)]


criterio7 = mod[['IdProy','m_proy_gastos','b_proy_gastos','desv_proy_gastos']].drop_duplicates()

dcontext7 = datos[(datos['TipoMov'].isin(['GTO', 'ACT']))]
dcontext7 = round(dcontext7.groupby(['IdProy' , 'mesi']).Monto.sum().to_frame()/1000000,3)
dcontext7 = dcontext7.reset_index()
dcontext7 = dcontext7.merge(criterio7,on = ['IdProy'], how = 'inner')
dcontext7['prom'] = dcontext7['m_proy_gastos'] * dcontext7['mesi'] + dcontext7['b_proy_gastos']
dcontext7['nivel+'] = dcontext7['prom'] + 2*dcontext7['desv_proy_gastos']
dcontext7['nivel-'] = dcontext7['prom'] - 2*dcontext7['desv_proy_gastos']
dcontext7.loc[dcontext7['Monto']<dcontext7['nivel-'],'alarma']='Gastos altos'
dcontext7.loc[dcontext7['Monto']>dcontext7['nivel+'],'alarma']='Gastos bajos'
dcontext7 = dcontext7[(dcontext7['alarma'].notnull())]
dcontext7 = dcontext7[['IdProy','mesi','Monto','prom','nivel+','nivel-','alarma']]


dcontext7 = dcontext7.reset_index(drop=True)
#dcontext7.to_feather(ruta+'alarmasQ1ProyGTO_BD.fth')
#dcontext7.to_excel(ruta+'alarmasQ1ProyGTO_BD.xlsx')
dcontext7
# %%
