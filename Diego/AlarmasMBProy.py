# %%

import pandas as pd
import feather as fd
import numpy as np
from datetime import datetime
ruta = 'C:/Users/AdministradorICS/Documents/'



mod = pd.read_feather(ruta+'ModeloProyMB_BD.fth')

datos = pd.read_feather(ruta+'DatosBD.feather')
datos = datos[(datos['mesi'] == 28)]

criterio2 = mod[['IdProy','m_proy_mb','b_proy_mb','desv_proy_mb']].drop_duplicates()

dcontext2 = datos
dcontext2 = round(dcontext2.groupby(['IdProy' , 'mesi']).Monto.sum().to_frame()/1000000,3)
dcontext2 = dcontext2.reset_index()
dcontext2 = dcontext2.merge(criterio2,on = ['IdProy'], how = 'inner')
dcontext2['prom'] = dcontext2['m_proy_mb'] * dcontext2['mesi'] + dcontext2['b_proy_mb']
dcontext2['nivel+'] = dcontext2['prom'] + 2*dcontext2['desv_proy_mb']
dcontext2['nivel-'] = dcontext2['prom'] - 2*dcontext2['desv_proy_mb']
dcontext2.loc[dcontext2['Monto']<dcontext2['nivel-'],'alarma']='MB bajo'
dcontext2.loc[dcontext2['Monto']>dcontext2['nivel+'],'alarma']='MB alto'
dcontext2 = dcontext2[(dcontext2['alarma'].notnull())]
dcontext2 = dcontext2[['IdProy','mesi','Monto','prom','nivel+','nivel-','alarma']]

dcontext2 = dcontext2.reset_index(drop=True)
#dcontext2.to_feather(ruta+'alarmasQ1ProyMB_BD.fth')
#dcontext2.to_excel(ruta+'alarmasQ1ProyMB_BD.xlsx')
dcontext2
# %%
