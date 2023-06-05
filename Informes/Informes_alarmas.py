# No me toma la importacion desde la carpeta principal:
import os
os.chdir(r'C:\\Users\\spannucio\\Desktop\\Proyecto-Anomalias\\ICS Anomalías\\Códigos_Análisis')

import pandas as pd
import feather as fd
import numpy as np

from Alarmas.Alarmas_Proy_Dia_Lineal import*
from Modelos_Alarmas.Alarma_Obras import*
from IPython.display import display

#====================================================================================================================
                              ### INFORMES DE LOS MODELOS DE ALARMAS POR PROYECTOS
# Quiero que me imprima las alarmas que se generaron de los modelos:
# No me los imprime me tira error de dataframe dias.# Consultar a Mario.
df_alarm_fac = alarmasfact()
df_mes = informemes()
df_media = informedia()

print("DataFrame de Alarma fact:")
display(df_alarm_fac) # No deberia usar "display" pero no se por que no me imprime en mi terminal los df

print("DataFrame de informe mes:")
display(df_mes)

print("DataFrame de Informe media:")
display(df_media)

# ==================================================================================================================
                              ## INFORME DE ALGUNAS ALARMAS POR OBRAS
# Verificamos que tipo de alarma hay:
if not alarmas_obras_mal_imputadas.empty or not obras_mayor.empty or not obras_menor.empty:
    # alarma-obra mal imputada:
    if not alarmas_obras_mal_imputadas.empty:
        num_proyectos = len(alarmas_obras_mal_imputadas['IdProy'].unique())

        print("ALARMA-Proyectos con obras mal imputadas:")
        print("Número de proyectos:", num_proyectos)
        print()

        for proyecto in alarmas_obras_mal_imputadas['IdProy'].unique():
            obras_proyecto = alarmas_obras_mal_imputadas[alarmas_obras_mal_imputadas['IdProy'] == proyecto]['ObraNro'].unique()
            nombres_obras = alarmas_obras_mal_imputadas[alarmas_obras_mal_imputadas['IdProy'] == proyecto]['ObraNombre'].unique()

            print("Proyecto:", proyecto)
            print("Obras:")
            for i in range(len(obras_proyecto)):
                print(" - Obra:", obras_proyecto[i])
                print("   Nombre:", nombres_obras[i])
            print()

    # alarma- margen bruto
    if not obras_mayor.empty or not obras_menor.empty:
        print("ALARMA-Obras con margen bruto fuera de lo habitual:")
        if not obras_mayor.empty:
            print("Obras con margen bruto más alto de lo habitual:")
            print(obras_mayor)
            print()
        if not obras_menor.empty:
            print("Obras con margen bruto más bajo de lo habitual:")
            print(obras_menor)
            print()
else:
    print("No se encontraron alarmas en obras, ni de obras mal imputadas ni obras con bajo-alto margen bruto.")
