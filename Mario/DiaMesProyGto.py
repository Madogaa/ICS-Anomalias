##           ##
##  PRUEBAS  ##
##           ##

# %%

from Alarmas.Alarmas_Proy_Mes import *
from Alarmas.Alarmas_Proy_Dia_Cuad import *

MES = 28
DIA = 31

ventasmes = alarmasventas(MES)
gastosmes = alarmasgastos(MES)
mbmes = alarmasmb(MES)
ventasdia = alarmasdiavta(MES,DIA)
gastosdia = alarmasdiagto(MES,DIA)

merged_df = pd.merge(ventasmes[['IdProy', 'alarma']], gastosmes[['IdProy', 'alarma']], on='IdProy', how='outer')
merged_df = pd.merge(merged_df, mbmes[['IdProy', 'alarma']], on='IdProy', how='outer')
merged_df = pd.merge(merged_df, ventasdia[['IdProy', 'alarma']], on='IdProy', how='outer')
merged_df = pd.merge(merged_df, gastosdia[['IdProy', 'alarma']], on='IdProy', how='outer')

# Renombramos las columnas de alarma para que sean distintas
merged_df.columns = ['proyecto', 'alarma1', 'alarma2', 'alarma3', 'alarma4', 'alarma5']
merged_df
# %%
