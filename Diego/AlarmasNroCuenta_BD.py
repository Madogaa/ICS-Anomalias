# %%

import pandas as pd
import feather as fd
import numpy as np
from datetime import datetime
ruta = 'C:/Users/AdministradorICS/Documents/'



mod = pd.read_feather(ruta+'ModeloNroCuenta_BD.fth')

datos = pd.read_feather(ruta+'DatosBD.feather')
datos = datos[(datos['mesi'] == 28)]


criterio3 = mod[['IdProy','CuentaNro','CuentaNombre','m_cuen','b_cuen','desv_cuen']]
# Convertir la columna 'CuentaNombre' de criterio3 a una cadena de texto
criterio3['CuentaNombre'] = criterio3['CuentaNombre'].astype(str)



NrosCuenta = [4210213,4210103,4210211,4210101,4210212,4210501]
dcontext3 = datos
dcontext3.loc[~dcontext3['CuentaNro'].isin(NrosCuenta),'CuentaNombre']='VARIOS'
dcontext3.loc[~dcontext3['CuentaNro'].isin(NrosCuenta),'CuentaNro']=1000000
dcontext3 = round(dcontext3.groupby(['IdProy','CuentaNro','mesi']).Monto.sum().to_frame()/1000000,3)
dcontext3 = dcontext3.reset_index()
dcontext3 = dcontext3.merge(criterio3,on = ['IdProy','CuentaNro'], how = 'inner')
dcontext3['prom'] = dcontext3['m_cuen'] * dcontext3['mesi'] + dcontext3['b_cuen']
dcontext3['nivel+'] = dcontext3['prom'] + 2*dcontext3['desv_cuen']
dcontext3['nivel-'] = dcontext3['prom'] - 2*dcontext3['desv_cuen']
dcontext3.loc[dcontext3['Monto']<dcontext3['nivel-'],'alarma']='Cuenta gasto alto'
dcontext3.loc[dcontext3['Monto']>dcontext3['nivel+'],'alarma']='Cuenta gasto bajo'
dcontext3 = dcontext3[(dcontext3['alarma'].notnull())]
dcontext3 = dcontext3[['IdProy','CuentaNro','CuentaNombre','mesi','Monto','prom','nivel+','nivel-','alarma']]


dcontext3 = dcontext3.reset_index(drop=True)
#dcontext3.to_feather(ruta+'alarmasQ1NroCuenta_BD.fth')
#dcontext3.to_excel(ruta+'alarmasQ1NroCuenta_BD.xlsx')
dcontext3
