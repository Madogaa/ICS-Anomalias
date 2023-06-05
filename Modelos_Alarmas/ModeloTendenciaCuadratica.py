# %%
import pandas as pd
import feather as fd
import numpy as np

#import os
#os.chdir(r'C:\Users\AdministradorICS\Desktop\GitAnomalias\ICS Anomalías\Códigos_Análisis')

# Importamos la base de datos filtrada desde el archivo principal:
from Datos.Base_datos import Filtro


#ruta = 'C:/Users/AdministradorICS/Documents/'
#all = pd.read_feather(ruta+'DatosBD.feather')

############            PROYECTO MB           ############

def tendenciaCuadraticaProy_MB():
    all=Filtro()
    lista=['IdProy','mesi']
    all = all[(all['mesi'] < 29)]
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
        coef = np.polyfit(data['x'], data['y'], deg=2)
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
tendenciaCuadraticaProy_MB_resultado = tendenciaCuadraticaProy_MB()


def ModeloCuadratico_MB ():
    all=Filtro()
    all = all[(all['mesi'] < 29 ) & (all['TipoMov'] == 'VTA')]
    all = round(all.groupby(['IdProy','mesi']).Monto.sum().to_frame()/1000000,3)
    all = all.reset_index()
    pred = tendenciaCuadraticaProy_MB()
    all = all.merge(pred,on=['IdProy'],how='inner')
    all['prom'] = (all['a'] * all['mesi']**2 + all['b'] * all['mesi'] + all['c'])
    all['nivel+'] = (all['a'] * all['mesi']**2 + all['b'] * all['mesi'] + all['c']) + 1.28 * all['desv']
    all['nivel-'] = (all['a'] * all['mesi']**2 + all['b'] * all['mesi'] + all['c']) - 1.28 * all['desv']
    return all

ModeloCuadratico_MB_resultado = ModeloCuadratico_MB()


############            PROYECTO VENTAS          ############

def tendenciaCuadraticaProy_VTA():
    all=Filtro()
    lista=['IdProy','mesi','TipoMov']
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
        coef = np.polyfit(data['x'], data['y'], deg=2)
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
tendenciaCuadraticaProy_VTA_resultado = tendenciaCuadraticaProy_VTA()

def ModeloCuadratico_VTA ():
    all=Filtro()
    all = all[(all['mesi'] < 29 ) & (all['TipoMov'] == 'VTA')]
    all = round(all.groupby(['IdProy','mesi']).Monto.sum().to_frame()/1000000,3)
    all = all.reset_index()
    pred = tendenciaCuadraticaProy_VTA()
    all = all.merge(pred,on=['IdProy'],how='inner')
    all['prom'] = (all['a'] * all['mesi']**2 + all['b'] * all['mesi'] + all['c'])
    all['nivel+'] = (all['a'] * all['mesi']**2 + all['b'] * all['mesi'] + all['c']) + 1.28 * all['desv']
    all['nivel-'] = (all['a'] * all['mesi']**2 + all['b'] * all['mesi'] + all['c']) - 1.28 * all['desv']
    return all


ModeloCuadratico_VTA_resultado = ModeloCuadratico_VTA()




# MODELO GASTOS POR PROYECTO #


def tendenciaCuadraticaProy_GTO():
    all=Filtro()
    lista=['IdProy','mesi','TipoMov']
    all = all[(all['mesi'] < 29) & (all['TipoMov'].isin(['GTO', 'ACT']))]  # Filtrar por GTO y ACT
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
        coef = np.polyfit(data['x'], data['y'], deg=2)
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
tendenciaCuadraticaProy_GTO_resultado = tendenciaCuadraticaProy_GTO()

def ModeloCuadratico_GTO ():
    all=Filtro()
    all = all[(all['mesi'] < 29) & (all['TipoMov'].isin(['GTO', 'ACT']))]
    all = round(all.groupby(['IdProy','mesi']).Monto.sum().to_frame()/1000000,3)
    all = all.reset_index()
    pred = tendenciaCuadraticaProy_GTO()
    all = all.merge(pred,on=['IdProy'],how='inner')
    all['prom'] = (all['a'] * all['mesi']**2 + all['b'] * all['mesi'] + all['c'])
    all['nivel+'] = (all['a'] * all['mesi']**2 + all['b'] * all['mesi'] + all['c']) + 1.28 * all['desv']
    all['nivel-'] = (all['a'] * all['mesi']**2 + all['b'] * all['mesi'] + all['c']) - 1.28 * all['desv']
    return all

ModeloCuadratico_GTO_resultado = ModeloCuadratico_GTO()

ModeloCuadratico_GTO_resultado


# %%
