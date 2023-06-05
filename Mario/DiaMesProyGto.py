# %%

#                                #
#   MODELO FACTURACION POR DIA   #
#                                #

import pandas as pd
import feather as fd
import numpy as np
import itertools

ruta = 'C:/Users/mario/Downloads/Practicas/'
ruta2 = 'C:/Users/mario/Downloads/Practicas/ModeloV3/ExcelT/'
all = pd.read_feather(ruta+'/ModeloV3/Python/datos.feather')
all = all[(all['mesi']< 28 ) & ((all['TipoMov'] == 'GTO') | (all['TipoMov'] == 'ACT'))]
lista = ['IdProy','mes']
lista1 = ['IdProy','mes','dia']
lista2 = ['IdProy','dia']

MESI_RNG = range(1, 28)
DIAS_RNG = range(1, 32)
NIVEL = 1.28 # 80% De los casos


vtaxmes = round(all.groupby(lista).Monto.sum().to_frame()/1000000,3)
vtaxmes = vtaxmes.rename(columns={'Monto':'VTAxMes'})
vtaxmes = vtaxmes.reset_index()


vtaxdia = round(all.groupby(lista1).Monto.sum().to_frame()/1000000,3)
vtaxdia = vtaxdia.rename(columns={'Monto':'VTAxDia'})
vtaxdia = vtaxdia.reset_index()

idproy = vtaxdia['IdProy'].unique()

all_combinations = pd.DataFrame(list(itertools.product(idproy,MESI_RNG,DIAS_RNG)),columns=['IdProy', 'mes', 'dia'])
all_combinations['VTAxDia'] = 0
merged = pd.merge(all_combinations, vtaxdia, how='outer', on=['IdProy', 'mes', 'dia'])
merged['VTAxDia_y'] = merged['VTAxDia_y'].fillna(0)
merged = merged.drop(['VTAxDia_x'],axis=1)
merged = merged.rename(columns={'VTAxDia_y':'VTAxDia'})

vtaxdia = merged

vtaxdiap = vtaxdia.merge(vtaxmes,on=['IdProy','mes'],how='inner')
vtaxdiap['Monto%'] = round((vtaxdiap['VTAxDia'] / vtaxdiap['VTAxMes']) * 100,1)
vtaxdiap['Monto'] = vtaxdiap.groupby(lista)['Monto%'].cumsum()
vtaxdiap = vtaxdiap.dropna(subset=['Monto'])

desv = vtaxdiap.groupby(by=lista2)['Monto'].std().to_frame()
desv = desv.rename(columns={'Monto':'desv'})
desv = desv.reset_index()
desv = desv.fillna(0)

promedio = vtaxdiap.groupby(by=lista2)['Monto'].mean().to_frame()
promedio = promedio.rename(columns={'Monto':'prom'})
promedio = promedio.reset_index()

promedio = promedio.merge(desv,on=['IdProy','dia'],how='inner')
promedio['nivel'] = promedio['prom'] + NIVEL * promedio['desv']
promedio.loc[promedio['nivel'] < 0 , 'nivel'] = 0
promedio.to_feather(ruta2+'promediogastossdia.fth')
# promedio.to_excel('temporal.xlsx')
promedio
# %%

#                                 #
#   ALARMAS FACTURACION POR DIA   #
#                                 #

import pandas as pd
import feather as fd
import numpy as np
import itertools

ruta = 'C:/Users/mario/Downloads/Practicas/'
ruta2 = 'C:/Users/mario/Downloads/Practicas/ModeloV3/ExcelT/'
all = pd.read_feather(ruta+'/ModeloV3/Python/datos.feather')

# 23-05-2023
MESI_MAX = 29 #MAYO DEL 2023
DIA_MAX= 31 # DIA 31

proyecto=[]
emptydia=[]

all = all[((all['mes'] == MESI_MAX) & (all['dia'] <= DIA_MAX)) & ((all['TipoMov'] == 'GTO') | (all['TipoMov'] == 'ACT'))]

mod = pd.read_feather(ruta2 + 'ModeloProyGastos_v2.fth')
prom = pd.read_feather(ruta2 + 'promediogastossdia.fth')

dias = round(all.groupby(['IdProy','dia']).Monto.sum().to_frame()/1000000,3).reset_index()
max_dia = dias.groupby('IdProy')['dia'].max().to_frame().reset_index()
for id in max_dia['IdProy']:
    d = max_dia[max_dia['IdProy'] == id]['dia']
    for dia in range(1, d.iloc[0]+1):
        input = dias[(dias['IdProy'] == id) & (dias['dia'] == dia)]
        if input.empty :
            proyecto.append(id)
            emptydia.append(dia)

diccionario = {'IdProy': proyecto,'dia': emptydia,'Monto': 0}
empty = pd.DataFrame(diccionario)
dias = pd.concat([dias,empty],axis=0).groupby(['IdProy','dia']).Monto.sum().to_frame().reset_index()
idproy= dias['IdProy'].unique()
dias = dias.merge(mod,on=['IdProy'],how='inner')
dias['GtoMes'] = dias['m_proy_gto'] * MESI_MAX + dias['b_proy_gto']
dias = dias.drop(['m_proy_gto','b_proy_gto','desv_proy_gto'],axis=1)
dias['Acum'] = dias.groupby(['IdProy'])['Monto'].cumsum()
dias['Gto%'] = (dias['Acum'] / dias['GtoMes'])  * 100
# dias = dias.drop(['Monto','Acum','GtoMes'],axis=1)
dias = dias.merge(prom,on=['IdProy','dia'],how='inner')
dias.loc[dias['Gto%'] > (dias['nivel']), 'alarma'] = 'Gasto adelantado'
dias = dias[dias['alarma'].notnull()].reset_index()
dias.to_feather('alarmasfacturacion.fth')
dias.to_excel('detalleInformeGastos29.xlsx')
dias
# %%

#                   #
#   TABLA INFORME   #
#                   #

import pandas as pd
import feather as fd

DIA_MAX = 31

rdatos = 'C:/Users/mario/Downloads/Practicas/ModeloV3/Datos.fth'
ruta = 'C:/Users/mario/Downloads/Practicas/ModeloV3/ExcelT/Pruebas/'

alarmas = pd.read_feather('alarmasfacturacion.fth').drop(['index'],axis=1)
idproy = alarmas['IdProy'].unique()

proyectos=[]
dias = []
al=[]

for id in idproy:
    for dia in range(1,DIA_MAX+1):
        temp = alarmas[(alarmas['IdProy'] == id) & (alarmas['dia'] == dia)]
        if not temp.empty:
            proyectos.append(id)
            dias.append(dia)
            al.append(1)
        else:
            proyectos.append(id)
            dias.append(dia)
            al.append(0)

diccionario = {'IdProy': proyectos ,'Dia': dias, 'Alarma': al}
df = pd.DataFrame(diccionario)
# Pivotar la tabla
pivot = df.pivot(index='IdProy', columns='Dia', values='Alarma').reset_index()
pivot.to_excel('C:/Users/mario/Downloads/Practicas/ModeloV3/ExcelT/Pruebas/'+'InfromeGastosDia29.xlsx')
pivot

# %%
