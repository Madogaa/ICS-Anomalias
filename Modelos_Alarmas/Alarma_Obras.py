# No me toma la importacion desde la carpeta principal:
import os
os.chdir(r'C:\\Users\\spannucio\\Desktop\\Proyecto-Anomalias\\ICS Anomalías\\Códigos_Análisis')

#===============================================================================
import pandas as pd
import feather as fd
import numpy as np
import warnings

#===============================================================================
warnings.filterwarnings("ignore", category=np.RankWarning)
warnings.filterwarnings("ignore", category=Warning)
# Importamos la base de datos filtrada desde el archivo principal:
from Datos.Base_datos import*

#==========================================================================================================
                                  ##### PRIMERA ALARMA- MARGEN BRUTO:

### Creamos función-Dataframe Margen Bruto:
def calcular_margen_bruto(df):
    df = df_Datos()
    # Se filtran los datos por ventas:
    df_ventas = df[df['TipoMov'] == 'VTA']
    ventas_sum = df_ventas.groupby('ObraNro')['Monto'].sum().reset_index()
    umbral_ventas = 0.001 #Valor minimo de ventas por  el monto de ventas es menor que el de gasto
    
    ## float
    df_ventas['Monto'] = df_ventas['Monto'].astype(float) 
    df_ventas['Monto'] = df_ventas['Monto'].abs()
    
    # Sumamos gastos + actuvos
    df_gto_act = df[(df['TipoMov'] == 'GTO') | (df['TipoMov'] == 'ACT')]
    gto_act_sum = df_gto_act.groupby('ObraNro')['Monto'].sum().reset_index()  
    
    #Montos abs de gst y act ya que no son valores todos negativos
    df_gto_act['Monto'] = df_gto_act['Monto'].astype(float) 
    df_gto_act['Monto'] = df_gto_act['Monto'].abs()

    # Datos de Vta,Gto y Act en funcion de la obra:
    df_merge = ventas_sum.merge(gto_act_sum, on='ObraNro', how='inner')

    # Filtramos datos###### Vemos como podemos mejorar esto:
    df_merge_filtered = df_merge[df_merge['Monto_x'] > umbral_ventas]

    # Calculamos el margen bruto
    margen_bruto = (df_merge_filtered['Monto_x'] + df_merge_filtered['Monto_y']) / df_merge_filtered['Monto_x']
    
    # Dataframe final:
    df_resultado = pd.DataFrame({
     'Obra': df_merge_filtered['ObraNro'],
     'Gastos_Activos': df_merge_filtered['Monto_y'],
     'Ventas': df_merge_filtered['Monto_x'],
     'MargenBruto': margen_bruto
    })

    # Calculamos el porcentaje
    df_resultado['%MBruto'] = (df_resultado['MargenBruto'] * 100).round(2)
    
    return df_resultado

Dto_Obra = df[['IdProy','ObraNro', 'Fecha', 'Fimp', 'TipoMov', 'Monto', 'ObraNombre']]
df_resultado = calcular_margen_bruto(Dto_Obra)
#df_resultado.head(3)

#==============================================================================================================
          ### Generamos alarma de Margen bruto alto o Bajo de las Obras:

def Obras_Alarma_MargenBruto(df_resultado):
    #Desviación/Promedio
    desviacion_estandar = df_resultado['MargenBruto'].std()
    margen_bruto_promedio = df_resultado['MargenBruto'].mean()

    #Calculamos e identificamos las obras con mayor margen bruto de lo habitual:
    limite_superior = margen_bruto_promedio + (2 * desviacion_estandar)
    obras_mayor_margen = df_resultado[df_resultado['MargenBruto'] > limite_superior]
    obras_mayor_margen['DesvioMargenBruto'] = obras_mayor_margen['MargenBruto'] - margen_bruto_promedio

    #Calculamos e identificamos las obras con menor margen bruto de lo habitual:
    limite_inferior = margen_bruto_promedio - (2 * desviacion_estandar) ##rango amplio que abarca aproximadamente el 95% de los datos
    obras_menor_margen = df_resultado[df_resultado['MargenBruto'] < limite_inferior]
    obras_menor_margen['DesvioMargenBruto'] = obras_menor_margen['MargenBruto'] - margen_bruto_promedio

    return obras_mayor_margen, obras_menor_margen

#Obras con margen bruto más alto o más bajo
obras_mayor, obras_menor = Obras_Alarma_MargenBruto(df_resultado)

#=================================================================================================================
                            #### SEGUNDA ALARMA- FECHA DE IMPUTACIÓN:
def obtener_alarmas_obras_mal_imputadas(df):
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    df['Fimp'] = pd.to_datetime(df['Fimp']) 
    df['Diferencia'] = df['Fimp'] - df['Fecha']
    df['Diferencia'] = df['Diferencia'].dt.days
    df['Alerta'] = np.where(df['Diferencia'] > 90, 'Alerta', 'Bien')
    alertas = df[df['Alerta'] == 'Alerta']
    
    return alertas
alarmas_obras_mal_imputadas = obtener_alarmas_obras_mal_imputadas(Dto_Obra)

#================================================================================================================
                                   #### GENERACIÓN DE ALARMA GENERICA:

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