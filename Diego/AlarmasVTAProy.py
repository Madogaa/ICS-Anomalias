# %%

import pandas as pd
import feather as fd
import numpy as np
from datetime import datetime
ruta = 'C:/Users/AdministradorICS/Documents/'



mod = pd.read_feather(ruta+'ModeloProyVentas_BD.fth')

datos = pd.read_feather(ruta+'DatosBD.feather')
datos = datos[(datos['mesi'] == 28)]


criterio1 = mod[['IdProy','m_proy_vta','b_proy_vta','desv_proy_vta']].drop_duplicates()

dcontext1 = datos[(datos['TipoMov'] == 'VTA')]
dcontext1 = round(dcontext1.groupby(['IdProy' , 'mesi']).Monto.sum().to_frame()/1000000,3)
dcontext1 = dcontext1.reset_index()
dcontext1 = dcontext1.merge(criterio1,on = ['IdProy'], how = 'inner')
dcontext1['prom'] = dcontext1['m_proy_vta'] * dcontext1['mesi'] + dcontext1['b_proy_vta']
dcontext1['nivel+'] = dcontext1['prom'] + 2*dcontext1['desv_proy_vta']
dcontext1['nivel-'] = dcontext1['prom'] - 2*dcontext1['desv_proy_vta']
dcontext1.loc[dcontext1['Monto']<dcontext1['nivel-'],'alarma']='Ventas bajas'
dcontext1.loc[dcontext1['Monto']>dcontext1['nivel+'],'alarma']='Ventas altas'
dcontext1 = dcontext1[(dcontext1['alarma'].notnull())]
dcontext1 = dcontext1[['IdProy','mesi','Monto','prom','nivel+','nivel-','alarma']]


dcontext1 = dcontext1.reset_index(drop=True)
#dcontext7.to_feather(ruta+'alarmasQ1ProyVTA_BD.fth')
#dcontext1.to_excel(ruta+'alarmasQ1ProyVTA_BD.xlsx')
dcontext1
# %%
