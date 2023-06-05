# %%
import os
os.chdir(r'C:\\Users\\mario\\OneDrive\\Documentos\\ICS Anomalías\\Códigos_Análisis')

import pandas as pd
import numpy as np
from Datos.Base_datos import*
import warnings

def promventas():
    all = Filtro()
    lista=['IdProy','mesi']
    all = all[(all['mesi'] < 29 ) & (all['TipoMov'] == 'VTA')]
    all = round(all.groupby(by=lista).Monto.sum().to_frame()/1000000,3)
    all = all.reset_index()
    idproy = all['IdProy'].unique()
    proyectos=[]
    lineaa = []
    lineab = []
    lineac = []
    desvio = []

    for id in idproy:
        # Crear un DataFrame con los datos
        proy = all[all['IdProy'] == id]
        data = pd.DataFrame({'x': proy['mesi'], 'y': proy['Monto']})
        # Calcular la regresión cuadrática
        with warnings.catch_warnings(record=True) as w:
            coef = np.polyfit(data['x'], data['y'], deg=2)
            if len(w) > 0:
                print(id)
                print(proy)
                print(w[0].message)
        a = coef[0]
        b = coef[1]
        c = coef[2]
        ###
        x = proy['mesi']
        y = proy['Monto']
        trendline = a * x**2 + b * x + c
        predicted = np.polyval(coef, x)
        residuals = y - predicted
        stdev = np.std(residuals)
        # Imprimir la regresión cuadrática
        proyectos.append(id)
        lineaa.append(a)
        lineab.append(b)
        lineac.append(c)
        desvio.append(stdev)

    diccionario = {'IdProy': idproy, 'a': lineaa,'b': lineab, 'c': lineac , 'desv': desvio}
    df = pd.DataFrame(diccionario)
    return df

def promgastos():
    all = Filtro()
    lista=['IdProy','mes']
    all = all[(all['mes'] < 29 ) & ((all['TipoMov'] == 'GTO') |(all['TipoMov'] == 'ACT'))]
    all = round(all.groupby(by=lista).Monto.sum().to_frame()/1000000,3)
    all = all.reset_index()
    idproy = all['IdProy'].unique()
    proyectos=[]
    lineaa = []
    lineab = []
    lineac = []
    desvio = []

    for id in idproy:
        # Crear un DataFrame con los datos
        proy = all[all['IdProy'] == id]
        data = pd.DataFrame({'x': proy['mes'], 'y': proy['Monto']})
        # Calcular la regresión cuadrática
        with warnings.catch_warnings(record=True) as w:
            coef = np.polyfit(data['x'], data['y'], deg=2)
            if len(w) > 0:
                print(id)
                print(proy)
                print(w[0].message)
        a = coef[0]
        b = coef[1]
        c = coef[2]
        ###
        x = proy['mes']
        y = proy['Monto']
        trendline = a * x**2 + b * x + c
        predicted = np.polyval(coef, x)
        residuals = y - predicted
        stdev = np.std(residuals)
        # Imprimir la regresión cuadrática
        proyectos.append(id)
        lineaa.append(a)
        lineab.append(b)
        lineac.append(c)
        desvio.append(stdev)

    diccionario = {'IdProy': idproy, 'a': lineaa,'b': lineab, 'c': lineac , 'desv': desvio}
    df = pd.DataFrame(diccionario)
    return df


def prommb():
    all = Filtro()
    lista=['IdProy','mesi']
    all = all[(all['mesi'] < 29 )]
    all = round(all.groupby(by=lista).Monto.sum().to_frame()/1000000,3)
    all = all.reset_index()
    idproy = all['IdProy'].unique()
    proyectos=[]
    lineaa = []
    lineab = []
    lineac = []
    desvio = []

    for id in idproy:
        # Crear un DataFrame con los datos
        proy = all[all['IdProy'] == id]
        data = pd.DataFrame({'x': proy['mesi'], 'y': proy['Monto']})
        # Calcular la regresión cuadrática
        with warnings.catch_warnings(record=True) as w:
            coef = np.polyfit(data['x'], data['y'], deg=2)
            if len(w) > 0:
                print(id)
                print(proy)
                print(w[0].message)
        a = coef[0]
        b = coef[1]
        c = coef[2]
        ###
        x = proy['mesi']
        y = proy['Monto']
        trendline = a * x**2 + b * x + c
        predicted = np.polyval(coef, x)
        residuals = y - predicted
        stdev = np.std(residuals)
        # Imprimir la regresión cuadrática
        proyectos.append(id)
        lineaa.append(a)
        lineab.append(b)
        lineac.append(c)
        desvio.append(stdev)

    diccionario = {'IdProy': idproy, 'a': lineaa,'b': lineab, 'c': lineac , 'desv': desvio}
    df = pd.DataFrame(diccionario)
    return df

df = promventas()
df
# %%
