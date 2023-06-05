# No me toma la importacion desde la carpeta principal:
import os
os.chdir(r'C:\\Users\\spannucio\\Desktop\\Proyecto-Anomalias\\ICS Anomalías\\Códigos_Análisis')

# Importación de librerias:
import pandas as pd
import numpy as np
# Importamos la base de datos filtrada desde el archivo principal:
from Datos.Base_datos import*


def modeloventas():
    all = Filtro()
    all = all[(all['mesi'] < 28 ) & (all['TipoMov'] == 'VTA')]
    all = round(all.groupby(['IdProy','mesi','TipoMov']).Monto.sum().to_frame()/1000000,3).reset_index()
    idproy = all['IdProy'].unique()

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

    diccionario = {'IdProy': idproy, 'm': lineam,'b': lineab , 'desv': desvio}
    df = pd.DataFrame(diccionario)
    return df

def modelogastos():
    all = Filtro()
    all = all[(all['mesi'] < 28) & ((all['TipoMov'] == 'GTO') | (all['TipoMov'] == 'ACT') )]
    all = round(all.groupby(['IdProy','mesi','TipoMov']).Monto.sum().to_frame()/1000000,3).reset_index()
    idproy = all['IdProy'].unique()

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

    diccionario = {'IdProy': idproy, 'm': lineam,'b': lineab , 'desv': desvio}
    df = pd.DataFrame(diccionario)
    return df

def modelomb():
    all = Filtro()
    all = all[(all['mesi'] < 28)]
    all = round(all.groupby(['IdProy','mesi']).Monto.sum().to_frame()/1000000,3).reset_index()
    idproy = all['IdProy'].unique()

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

    diccionario = {'IdProy': idproy, 'm': lineam,'b': lineab , 'desv': desvio}
    df = pd.DataFrame(diccionario)
    return df