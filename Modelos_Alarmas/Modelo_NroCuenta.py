# %%
import os
os.chdir(r'C:\\Users\\mario\\OneDrive\\Documentos\\ICS Anomalías\\Códigos_Análisis')

import pandas as pd
from Datos.Base_datos import*
import numpy as np
import warnings

def modelo_nrocue():
    all = Filtro()
    all = all[(all['mesi']<29)]
    lista=['IdProy','CuentaNro','CuentaNombre','mesi']

    NrosCuenta = ['4110101','4210213','4210103','4210211','4210101','4210212','4210501']
    NrosCuentaT = ['4110101','4210213','4210103','4210211','4210101','4210212','4210501','1000000']
    all['CuentaNombre'] = all['CuentaNombre'].str.strip()

    nrocu = round(all.groupby(by=lista).Monto.sum().to_frame()/1000000,3).reset_index()
    nrocu.loc[~nrocu['CuentaNro'].isin(NrosCuenta),'CuentaNombre']='VARIOS'
    nrocu.loc[~nrocu['CuentaNro'].isin(NrosCuenta),'CuentaNro']='1000000'
    idproy = nrocu['IdProy'].unique()

    proyectos = []
    cuentas = []
    coefa = []
    coefb = []
    coefc = []
    desvio = []
    nombres = []

    for id in idproy:
        for cu in NrosCuentaT:
            # Crear un DataFrame con los datos
            proy = nrocu[(nrocu['IdProy'] == id ) & (nrocu['CuentaNro'] == cu )]
            if not proy.empty :
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
                # Imprimir la línea de tendencia
                proyectos.append(id)
                cuentas.append(cu)
                nombres.append(proy['CuentaNombre'].unique())
                coefa.append(a)
                coefb.append(b)
                coefc.append(c)
                desvio.append(stdev)

    diccionario = {'IdProy': proyectos, 'CuentaNro': cuentas ,'a': coefa,'b': coefb ,'c' : coefc, 'desv': desvio}
    df = pd.DataFrame(diccionario)
    return df

df = modelo_nrocue()
df
# %%
