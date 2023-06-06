# %%

import os
os.chdir(r'C:\\Users\\mario\\OneDrive\\Documentos\\ICS Anomalías\\Códigos_Análisis')

import pandas as pd
import numpy as np
import warnings
from Datos.Base_datos import *

def modelo_nrocc():
    all = FiltroFinal()
    all = all[(all['mesi']<29)]
    lista = ['NroCC_Obra', 'NombreCC_Obra', 'mesi']
    nrocu = round(all.groupby(by=lista).MONTO.sum().to_frame() / 1000000, 3).reset_index()
    nrocu = nrocu[nrocu['NroCC_Obra'].str.startswith('1')]

    nroscc = nrocu['NroCC_Obra'].unique()

    cuentas = []
    coefa = []
    coefb = []
    coefc = []
    desvio = []
    nombres = []

    for id in nroscc:
        # Crear un DataFrame con los datos
        proy = nrocu[(nrocu['NroCC_Obra'] == id )]
        if not proy.empty :
            data = pd.DataFrame({'x': proy['mesi'], 'y': proy['MONTO']})
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
            y = proy['MONTO']
            trendline = a * x**2 + b * x + c
            predicted = np.polyval(coef, x)
            residuals = y - predicted
            stdev = np.std(residuals)
            # Imprimir la línea de tendencia
            cuentas.append(id)
            nombres.append(proy['NroCC_Obra'].unique())
            coefa.append(a)
            coefb.append(b)
            coefc.append(c)
            desvio.append(stdev)

    diccionario = {'NroCC_Obra': cuentas ,'a': coefa,'b': coefb ,'c' : coefc, 'desv': desvio}
    df = pd.DataFrame(diccionario)
    return df

df = modelo_nrocc()
df
# %%
