# %%
import os
os.chdir(r'C:\\Users\\mario\\OneDrive\Documentos\\AnomaliasICS\\Códigos_Análisis')
ruta = 'C:/Users/mario/OneDrive/Documentos/AnomaliasICS/Códigos_Análisis/Modelos_Feather/'
import pandas as pd
from Modelos_Alarmas.Modelo_Proy_Mes_Cuad import *
from Modelos_Alarmas.Modelo_Proy_Dia_Cuad import *
from Modelos_Alarmas.Modelo_NroCuenta import *
from Modelos_Alarmas.Modelo_NroCC import *
from Modelos_Alarmas.Modelo_NroCC_Dia import *

modelo = modelo_nrocc_dia()
modelo.to_feather(ruta+ 'Modelo_NroCC_Dia.fth')
modelo
# %%
