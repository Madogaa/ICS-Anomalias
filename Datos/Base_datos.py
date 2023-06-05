# %%
# Importación de librerias:
import pandas as pd
import pyodbc

# Base de datos conectada desde sql server:
def df_Datos():
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=dbtstanalytics.database.windows.net;DATABASE=tstanalytics;UID=analyticsreader;PWD=@q$eQX89Xp7yUEm')# Creamos la consulta:
    df = pd.read_sql_query('SELECT * FROM Output_EstadoDeResultados', conn )
    return df

def act_date(df):
    fecha = df['Fecha'].max()
    fecha = pd.to_datetime(fecha)
    fecha = fecha.strftime('%Y-%m-%d')
    return fecha

# Filtro de la base de datos, de la meses y fecha de imputacion:
## Tratamiento de datos:
def Filtro():
    df= df_Datos()
    df['mesi'] = df['Fimp'].dt.month + 12*(df['Fimp'].dt.year-2021)
    df['añoi'] = df['Fimp'].dt.year
    df['diai'] = df['Fimp'].dt.day
    df['mes'] = df['Fecha'].dt.month + 12*(df['Fimp'].dt.year-2021)
    df['año'] = df['Fecha'].dt.year
    df['dia'] = df['Fecha'].dt.day
    print(act_date(df))
    return df

df = Filtro()
#Se imprime el filtrado
# %%
