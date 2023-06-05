#%%
import pyodbc
import pandas as pd
import feather as fd
# Nos conectamos a la base de datos y generamos un archivo feather

conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=dbtstanalytics.database.windows.net;DATABASE=tstanalytics;UID=analyticsreader;PWD=@q$eQX89Xp7yUEm')

cursor = conn.cursor() # se crea el cursor para la conexión

ruta = 'C:/Users/AdministradorICS/Documents/'


# Creamos la consulta:

df1 = pd.read_sql_query('SELECT * FROM Output_EstadoDeResultados', conn )




# De dataframe pasamos a formato feather:

df1.to_feather(ruta+'ModeloBD.feather')

df=pd.read_feather(ruta+'ModeloBD.feather')

df.head(3)


#%%
# AÑADIMOS EL MES Y EL AÑO AL FEATHER DE LA BASE DE DATOS
import pandas as pd
ruta = 'C:/Users/AdministradorICS/Documents/'
datos=pd.read_feather(ruta+'ModeloBD.feather')

datos['mesi'] = datos['Fimp'].dt.month + 12*(datos['Fimp'].dt.year-2021)
datos['añoi'] = all['Fimp'].dt.year
datos.to_feather(ruta+'DatosBD.feather')
datos

# %%
############            OBRAS NORMALES              ############



# %%

#                           #
#                           #
#       MARGEN BRUTO OBRAS        #
#                           #
#                           #

import pandas as pd
import feather as fd
import numpy as np

ruta = 'C:/Users/AdministradorICS/Documents/'
all = pd.read_feather(ruta+'DatosBD.feather')
all = all[((all ['mesi'] < 28))]
obgto0 = all.groupby('ObraNro').filter(lambda x: (x['TipoMov'] == 'VTA').all() and not x['TipoMov'].isin(['GTO', 'ACT']).any())
obvta0 = all.groupby('ObraNro').filter(lambda x: (x['TipoMov'].isin(['GTO', 'ACT'])).all() and not (x['TipoMov'] == 'VTA').any())
obrasvta0 = (obvta0.groupby('ObraNro').Monto.sum().to_frame()/1000000).reset_index()
obrasgto0 = (obgto0.groupby('ObraNro').Monto.sum().to_frame()/1000000).reset_index()
obvtagto0 = pd.concat([obrasgto0['ObraNro'], obrasvta0['ObraNro']])
obnorm = all[~all['ObraNro'].isin(obvtagto0)]
obgto0['Descripcion'] = 'OBRA GASTO 0'
obvta0['Descripcion'] = 'OBRA VENTAS 0'
obnorm['Descripcion'] = 'OBRA NORMAL'

lista=['IdProy','ObraNro','Fecha']
lista1=['IdProy','Descripcion']
idproy = [46,20,3,6,40,4,13,66,87,91,85]

obras = round(obnorm.groupby(by=lista).Monto.sum().to_frame()/1000000,3)
obras = obras.reset_index()
obras['min'] = obras.groupby(['IdProy','ObraNro'])['Fecha'].transform(min)
obras['max'] = obras.groupby(['IdProy','ObraNro'])['Fecha'].transform(max)
obras['FechaAvg'] = obras[['min', 'max']].mean(axis=1)
obras['FechaAvg'] = pd.to_datetime((obras['min'].values.astype(np.int64) + obras['max'].values.astype(np.int64)) // 2)
obras['Dias'] = obras['FechaAvg'] - pd.Timestamp('2021-01-01')
obras['Dias'] = obras['Dias'].dt.days
obras['FechaAvg'] = obras['FechaAvg'].dt.strftime('%d/%m/%Y')
obras = obras.drop(['Fecha','min','max'],axis=1)
obras = obras[['IdProy','FechaAvg','Dias','ObraNro','Monto']]
obras = obras.groupby(['IdProy','Dias','ObraNro']).Monto.sum().to_frame()
obras = obras.reset_index()

proyectos = []
lineam = []
lineab = []
desvio = []


for id in idproy:
     # Crear un DataFrame con los datos
    proy = obras[(obras['IdProy'] == id )]
    if not proy.empty :
        data = pd.DataFrame({'x': proy['Dias'], 'y': proy['Monto']})
        # Calcular la línea de tendencia
        coef = np.polyfit(data['x'], data['y'], deg=1)
        m = coef[0]
        b = coef[1]
        ###
        x = proy['Dias']
        y = proy['Monto']
        trendline = m * x + b
        predicted = np.polyval(coef, x)
        residuals = y - predicted
        stdev = np.std(residuals)
        # Imprimir la línea de tendencia
        proyectos.append(id)
        lineam.append(m)
        lineab.append(b)
        desvio.append(stdev)

diccionario = {'IdProy': proyectos,'m': lineam,'b': lineab , 'desv': desvio}
df = pd.DataFrame(diccionario)
df['Descripcion'] = 'OBRAS NORMALES'
#df.to_feather(ruta2+'Excel/ModeloObrasMB_v2.fth')
#df.to_excel(ruta2+'Excel/ModeloObrasMB_v2.xlsx')
df

# %%

#                   #
#                   #
#       VENTAS  OBRAS    #
#                   #
#                   #

import pandas as pd
import feather as fd
import numpy as np

ruta = 'C:/Users/AdministradorICS/Documents/'
all = pd.read_feather(ruta+'DatosBD.feather')
all = all[((all ['mesi'] < 28))]
obgto0 = all.groupby('ObraNro').filter(lambda x: (x['TipoMov'] == 'VTA').all() and not x['TipoMov'].isin(['GTO', 'ACT']).any())
obvta0 = all.groupby('ObraNro').filter(lambda x: (x['TipoMov'].isin(['GTO', 'ACT'])).all() and not (x['TipoMov'] == 'VTA').any())
obrasvta0 = (obvta0.groupby('ObraNro').Monto.sum().to_frame()/1000000).reset_index()
obrasgto0 = (obgto0.groupby('ObraNro').Monto.sum().to_frame()/1000000).reset_index()
obvtagto0 = pd.concat([obrasgto0['ObraNro'], obrasvta0['ObraNro']])
obnorm = all[~all['ObraNro'].isin(obvtagto0)]
obgto0['Descripcion'] = 'OBRA GASTO 0'
obvta0['Descripcion'] = 'OBRA VENTAS 0'
obnorm['Descripcion'] = 'OBRA NORMAL'

lista=['IdProy','ObraNro','Fecha']
lista1=['IdProy','Descripcion']
idproy = [46,20,3,6,40,4,13,66,87,91,85]

obnorm = obnorm[obnorm['TipoMov'] == 'VTA']

obras = round(obnorm.groupby(by=lista).Monto.sum().to_frame()/1000000,3)
obras = obras.reset_index()
obras['min'] = obras.groupby(['IdProy','ObraNro'])['Fecha'].transform(min)
obras['max'] = obras.groupby(['IdProy','ObraNro'])['Fecha'].transform(max)
obras['FechaAvg'] = obras[['min', 'max']].mean(axis=1)
obras['Dias'] = obras['FechaAvg'] - pd.Timestamp('2021-01-01')
obras['Dias'] = obras['Dias'].dt.days
obras['FechaAvg'] = obras['FechaAvg'].dt.strftime('%d/%m/%Y')
obras = obras.drop(['Fecha','min','max'],axis=1)
obras = obras[['IdProy','FechaAvg','Dias','ObraNro','Monto']]
obras = obras.groupby(['IdProy','Dias','ObraNro']).Monto.sum().to_frame()
obras = obras.reset_index()

proyectos = []
lineam = []
lineab = []
desvio = []


for id in idproy:
     # Crear un DataFrame con los datos
    proy = obras[(obras['IdProy'] == id )]
    if not proy.empty :
        data = pd.DataFrame({'x': proy['Dias'], 'y': proy['Monto']})
        # Calcular la línea de tendencia
        coef = np.polyfit(data['x'], data['y'], deg=1)
        m = coef[0]
        b = coef[1]
        ###
        x = proy['Dias']
        y = proy['Monto']
        trendline = m * x + b
        predicted = np.polyval(coef, x)
        residuals = y - predicted
        stdev = np.std(residuals)
        # Imprimir la línea de tendencia
        proyectos.append(id)
        lineam.append(m)
        lineab.append(b)
        desvio.append(stdev)

diccionario = {'IdProy': proyectos,'m': lineam,'b': lineab , 'desv': desvio}
df = pd.DataFrame(diccionario)
df['Descripcion'] = 'OBRAS NORMALES'
#df.to_feather(ruta2+'Excel/ModeloObrasVentas_v2.fth')
#df.to_excel(ruta2+'Excel/ModeloObrasVentas_v2.xlsx')
df
# %%

############            OBRAS VTA 0              ############

# %%
import pandas as pd
import feather as fd
import numpy as np

ruta = 'C:/Users/AdministradorICS/Documents/'
all = pd.read_feather(ruta+'DatosBD.feather')
all = all[((all ['mesi'] < 28))]
obgto0 = all.groupby('ObraNro').filter(lambda x: (x['TipoMov'] == 'VTA').all() and not x['TipoMov'].isin(['GTO', 'ACT']).any())
obvta0 = all.groupby('ObraNro').filter(lambda x: (x['TipoMov'].isin(['GTO', 'ACT'])).all() and not (x['TipoMov'] == 'VTA').any())
obrasvta0 = (obvta0.groupby('ObraNro').Monto.sum().to_frame()/1000000).reset_index()
obrasgto0 = (obgto0.groupby('ObraNro').Monto.sum().to_frame()/1000000).reset_index()
obvtagto0 = pd.concat([obrasgto0['ObraNro'], obrasvta0['ObraNro']])
obnorm = all[~all['ObraNro'].isin(obvtagto0)]
obgto0['Descripcion'] = 'OBRA GASTO 0'
obvta0['Descripcion'] = 'OBRA VENTAS 0'
obnorm['Descripcion'] = 'OBRA NORMAL'

lista=['IdProy','ObraNro','Fecha']
lista1=['IdProy','Descripcion']
idproy = [46,20,3,6,40,4,13,66,87,91,85]

obras = round(obvta0.groupby(by=lista).Monto.sum().to_frame()/1000000,3)
obras = obras.reset_index()
obras['min'] = obras.groupby(['IdProy','ObraNro'])['Fecha'].transform(min)
obras['max'] = obras.groupby(['IdProy','ObraNro'])['Fecha'].transform(max)
obras['FechaAvg'] = obras[['min', 'max']].mean(axis=1)
obras['FechaAvg'] = pd.to_datetime((obras['min'].values.astype(np.int64) + obras['max'].values.astype(np.int64)) // 2)
obras['Dias'] = obras['FechaAvg'] - pd.Timestamp('2021-01-01')
obras['Dias'] = obras['Dias'].dt.days
obras['FechaAvg'] = obras['FechaAvg'].dt.strftime('%d/%m/%Y')
obras = obras.drop(['Fecha','min','max'],axis=1)
obras = obras[['IdProy','FechaAvg','Dias','ObraNro','Monto']]
obras = obras.groupby(['IdProy','Dias','ObraNro']).Monto.sum().to_frame()
obras = obras.reset_index()

proyectos = []
lineam = []
lineab = []
desvio = []


for id in idproy:
     # Crear un DataFrame con los datos
    proy = obras[(obras['IdProy'] == id )]
    if not proy.empty :
        data = pd.DataFrame({'x': proy['Dias'], 'y': proy['Monto']})
        # Calcular la línea de tendencia
        coef = np.polyfit(data['x'], data['y'], deg=1)
        m = coef[0]
        b = coef[1]
        ###
        x = proy['Dias']
        y = proy['Monto']
        trendline = m * x + b
        predicted = np.polyval(coef, x)
        residuals = y - predicted
        stdev = np.std(residuals)
        # Imprimir la línea de tendencia
        proyectos.append(id)
        lineam.append(m)
        lineab.append(b)
        desvio.append(stdev)

diccionario = {'IdProy': proyectos,'m_obv0': lineam,'b_obv0': lineab , 'desv_obv0': desvio}
df = pd.DataFrame(diccionario)
df['Descripcion'] = 'OBRAS VENTAS 0'
df.to_feather(ruta+'ModeloObrasVentasTipo0_v2Final.fth')
#df.to_excel(ruta2+'Excel/ModeloObrasVentasTipo0_v2.xlsx')
df
# %%

############            OBRAS GTO 0              ############

# %%
import pandas as pd
import feather as fd
import numpy as np

ruta = 'C:/Users/AdministradorICS/Documents/'
all = pd.read_feather(ruta+'DatosBD.feather')
all = all[((all ['mesi'] < 28))]
obgto0 = all.groupby('ObraNro').filter(lambda x: (x['TipoMov'] == 'VTA').all() and not x['TipoMov'].isin(['GTO', 'ACT']).any())
obvta0 = all.groupby('ObraNro').filter(lambda x: (x['TipoMov'].isin(['GTO', 'ACT'])).all() and not (x['TipoMov'] == 'VTA').any())
obrasvta0 = (obvta0.groupby('ObraNro').Monto.sum().to_frame()/1000000).reset_index()
obrasgto0 = (obgto0.groupby('ObraNro').Monto.sum().to_frame()/1000000).reset_index()
obvtagto0 = pd.concat([obrasgto0['ObraNro'], obrasvta0['ObraNro']])
obnorm = all[~all['ObraNro'].isin(obvtagto0)]
obgto0['Descripcion'] = 'OBRA GASTO 0'
obvta0['Descripcion'] = 'OBRA VENTAS 0'
obnorm['Descripcion'] = 'OBRA NORMAL'

lista=['IdProy','ObraNro','Fecha']
lista1=['IdProy','Descripcion']
idproy = [46,20,3,6,40,4,13,66,87,91,85]

obras = round(obgto0.groupby(by=lista).Monto.sum().to_frame()/1000000,3)
obras = obras.reset_index()
obras['min'] = obras.groupby(['IdProy','ObraNro'])['Fecha'].transform(min)
obras['max'] = obras.groupby(['IdProy','ObraNro'])['Fecha'].transform(max)
obras['FechaAvg'] = obras[['min', 'max']].mean(axis=1)
obras['FechaAvg'] = pd.to_datetime((obras['min'].values.astype(np.int64) + obras['max'].values.astype(np.int64)) // 2)
obras['Dias'] = obras['FechaAvg'] - pd.Timestamp('2021-01-01')
obras['Dias'] = obras['Dias'].dt.days
obras['FechaAvg'] = obras['FechaAvg'].dt.strftime('%d/%m/%Y')
obras = obras.drop(['Fecha','min','max'],axis=1)
obras = obras[['IdProy','FechaAvg','Dias','ObraNro','Monto']]
obras = obras.groupby(['IdProy','Dias','ObraNro']).Monto.sum().to_frame()
obras = obras.reset_index()

proyectos = []
lineam = []
lineab = []
desvio = []


for id in idproy:
     # Crear un DataFrame con los datos
    proy = obras[(obras['IdProy'] == id )]
    if not proy.empty :
        data = pd.DataFrame({'x': proy['Dias'], 'y': proy['Monto']})
        # Calcular la línea de tendencia
        coef = np.polyfit(data['x'], data['y'], deg=1)
        m = coef[0]
        b = coef[1]
        ###
        x = proy['Dias']
        y = proy['Monto']
        trendline = m * x + b
        predicted = np.polyval(coef, x)
        residuals = y - predicted
        stdev = np.std(residuals)
        # Imprimir la línea de tendencia
        proyectos.append(id)
        lineam.append(m)
        lineab.append(b)
        desvio.append(stdev)

diccionario = {'IdProy': proyectos,'m_obg0': lineam,'b_obg0': lineab , 'desv_obg0': desvio}
df = pd.DataFrame(diccionario)
df['Descripcion'] = 'OBRAS GASTOS 0'
df.to_feather(ruta+'ModeloObrasGastosTipo0_v2Final.fth')
#df.to_excel(ruta+'ModeloObrasGastosTipo0_v2Final.xlsx')
df

# %%

############            NRO DE CUENTA              ############


import pandas as pd
import feather as fd
import numpy as np

ruta = 'C:/Users/AdministradorICS/Documents/'
all = pd.read_feather(ruta+'DatosBD.feather')
all = all[(all['mesi']<28)]
lista=['IdProy','CuentaNro','CuentaNombre','mesi']
lista1=['IdProy','CuentaNro','CuentaNombre']

NrosCuenta = [4210213,4210103,4210211,4210101,4210212,4210501]
NrosCuentaT = [4210213,4210103,4210211,4210101,4210212,4210501,1000000]
all['CuentaNombre'] = all['CuentaNombre'].str.strip()

nrocu = round(all.groupby(by=lista).Monto.sum().to_frame()/1000000,3)
nrocu = nrocu.reset_index()
nrocu.loc[~nrocu['CuentaNro'].isin(NrosCuenta),'CuentaNombre']='VARIOS'
nrocu.loc[~nrocu['CuentaNro'].isin(NrosCuenta),'CuentaNro']=1000000

idproy = [46,20,3,6,40,4,13,66,87,91,85]

proyectos = []
cuentas = []
lineam = []
lineab = []
desvio = []
nombres = []

for id in idproy:
    for cu in NrosCuentaT:
        # Crear un DataFrame con los datos
        proy = nrocu[(nrocu['IdProy'] == id ) & (nrocu['CuentaNro'] == cu )]
        if not proy.empty :
            data = pd.DataFrame({'x': proy['mesi'], 'y': proy['Monto']})
            # Calcular la línea de tendencia
            coef = np.polyfit(data['x'], data['y'], deg=1)
            m = coef[0]
            b = coef[1]
            ###
            x = proy['mesi']
            y = proy['Monto']
            trendline = m * x + b
            predicted = np.polyval(coef, x)
            residuals = y - predicted
            stdev = np.std(residuals)
            # Imprimir la línea de tendencia
            proyectos.append(id)
            cuentas.append(cu)
            nombres.append(proy['CuentaNombre'].unique())
            lineam.append(m)
            lineab.append(b)
            desvio.append(stdev)

diccionario = {'IdProy': proyectos, 'CuentaNro': cuentas, 'CuentaNombre': nombres ,'m_cuen': lineam,'b_cuen': lineab , 'desv_cuen': desvio}
df = pd.DataFrame(diccionario)
df.to_feather(ruta+'ModeloNroCuenta_BD.fth')


df

# %%

############            PROYECTO MB           ############

# %%

import pandas as pd
import numpy as np

ruta = 'C:/Users/AdministradorICS/Documents/'
all = pd.read_feather(ruta+'DatosBD.feather')
lista=['IdProy','mesi']
all = all[(all['mesi'] < 28)]
all = round(all.groupby(by=lista).Monto.sum().to_frame()/1000000,3)
all = all.reset_index()
idproy = [46,20,3,6,40,4,13,66,87,91,85]

lineam = []
lineab = []
desvio = []

for id in idproy:
    # Crear un DataFrame con los datos
    proy = all[all['IdProy'] == id]
    data = pd.DataFrame({'x': proy['mesi'], 'y': proy['Monto']})
    # Calcular la línea de tendencia
    coef = np.polyfit(data['x'], data['y'], deg=1)
    m = coef[0]
    b = coef[1]
    ###
    x = proy['mesi']
    y = proy['Monto']
    trendline = m * x + b
    predicted = np.polyval(coef, x)
    residuals = y - predicted
    stdev = np.std(residuals)
    # Imprimir la línea de tendencia
    lineam.append(m)
    lineab.append(b)
    desvio.append(stdev)

diccionario = {'IdProy': idproy, 'm_proy_mb': lineam,'b_proy_mb': lineab , 'desv_proy_mb': desvio}
df = pd.DataFrame(diccionario)
df.to_feather(ruta+'ModeloProyMB_BD.fth')
df

# %%

############            PROYECTO VENTAS          ############

import pandas as pd
import numpy as np

ruta = 'C:/Users/AdministradorICS/Documents/'
all = pd.read_feather(ruta+'DatosBD.feather')
lista=['IdProy','mesi']
all = all[(all['mesi'] < 28) & (all['TipoMov'] == 'VTA')]
all = round(all.groupby(by=lista).Monto.sum().to_frame()/1000000,3)
all = all.reset_index()
idproy = [46,20,3,6,40,4,13,66,87,91,85]

lineam = []
lineab = []
desvio = []

for id in idproy:
    # Crear un DataFrame con los datos
    proy = all[all['IdProy'] == id]
    data = pd.DataFrame({'x': proy['mesi'], 'y': proy['Monto']})
    # Calcular la línea de tendencia
    coef = np.polyfit(data['x'], data['y'], deg=1)
    m = coef[0]
    b = coef[1]
    ###
    x = proy['mesi']
    y = proy['Monto']
    trendline = m * x + b
    predicted = np.polyval(coef, x)
    residuals = y - predicted
    stdev = np.std(residuals)
    # Imprimir la línea de tendencia
    lineam.append(m)
    lineab.append(b)
    desvio.append(stdev)

diccionario = {'IdProy': idproy, 'm_proy_vta': lineam,'b_proy_vta': lineab , 'desv_proy_vta': desvio}
df = pd.DataFrame(diccionario)
df.to_feather(ruta+'ModeloProyVentas_BD.fth')
df

# %%

# MODELO GASTOS POR PROYECTO #


import pandas as pd
import numpy as np

ruta = 'C:/Users/AdministradorICS/Documents/'
all = pd.read_feather(ruta+'DatosBD.feather')
lista=['IdProy','mesi']
all = all[(all['mesi'] < 28) & (all['TipoMov'].isin(['GTO', 'ACT']))]  # Filtrar por GTO y ACT
all = round(all.groupby(by=lista).Monto.sum().to_frame()/1000000,3)
all = all.reset_index()
idproy = [46,20,3,6,40,4,13,66,87,91,85]

lineam = []
lineab = []
desvio = []

for id in idproy:
    # Crear un DataFrame con los datos
    proy = all[all['IdProy'] == id]
    data = pd.DataFrame({'x': proy['mesi'], 'y': proy['Monto']})
    # Calcular la línea de tendencia
    coef = np.polyfit(data['x'], data['y'], deg=1)
    m = coef[0]
    b = coef[1]
    ###
    x = proy['mesi']
    y = proy['Monto']
    trendline = m * x + b
    predicted = np.polyval(coef, x)
    residuals = y - predicted
    stdev = np.std(residuals)
    # Imprimir la línea de tendencia
    lineam.append(m)
    lineab.append(b)
    desvio.append(stdev)

diccionario = {'IdProy': idproy, 'm_proy_gastos': lineam, 'b_proy_gastos': lineab, 'desv_proy_gastos': desvio}
df = pd.DataFrame(diccionario)
df.to_feather(ruta+'ModeloProyGastos_BD.fth')
df
