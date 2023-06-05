import pandas as pd
import feather as fd
import numpy as np
import datetime
from Datos.Base_datos import*
from Modelos_Alarmas.Modelo_Proy_Mes_Lineal import*
from Modelos_Alarmas.Modelo_Proy_Dia_Lineal import*

def alarmasfact():
    MESI_MAX = 29
    DIA_MAX= 31

    all = Filtro()
    all = all[((all['mesi'] == MESI_MAX) & (all['diai'] <= DIA_MAX)) & (all['TipoMov'] == 'VTA') & (all['Monto'] >= 0)]

    proyecto=[]
    emptydia=[]
    mod = modeloventas()
    prom = promdiafact()

    dias = round(all.groupby(['IdProy','diai']).Monto.sum().to_frame()/1000000,3).reset_index()
    max_diai = dias.groupby('IdProy')['diai'].max().to_frame().reset_index()
    for id in max_diai['IdProy']:
        d = max_diai[max_diai['IdProy'] == id]['diai']
        for dia in range(1, d.iloc[0]+1):
            input = dias[(dias['IdProy'] == id) & (dias['diai'] == dia)]
            if input.empty :
                proyecto.append(id)
                emptydia.append(dia)

    diccionario = {'IdProy': proyecto,'diai': emptydia,'Monto': 0}
    empty = pd.DataFrame(diccionario)
    dias = pd.concat([dias,empty],axis=0).groupby(['IdProy','diai']).Monto.sum().to_frame().reset_index()
    dias = dias.merge(mod,on=['IdProy'],how='inner')
    dias['VtaMes'] = dias['m_proy_vta'] * MESI_MAX + dias['b_proy_vta']
    dias = dias.drop(['m_proy_vta','b_proy_vta','desv_proy_vta'],axis=1)
    dias['Acum'] = dias.groupby(['IdProy'])['Monto'].cumsum()
    dias['Vta%'] = (dias['Acum'] / dias['VtaMes'])  * 100
    dias = dias.merge(prom,on=['IdProy','diai'],how='inner')
    dias.loc[dias['Vta%'] < (dias['nivel']), 'alarma'] = 'Facturacion retrasada'
    dias = dias[dias['alarma'].notnull()].reset_index()
    return dias

def informemes():
    DIA_MAX = 31

    alarmas = alarmasfact()
    idproy = alarmas['IdProy'].unique()

    proyectos=[]
    dias = []
    al=[]

    for id in idproy:
        for dia in range(1,DIA_MAX+1):
            temp = alarmas[(alarmas['IdProy'] == id) & (alarmas['diai'] == dia)]
            if not temp.empty:
                proyectos.append(id)
                dias.append(dia)
                al.append(1)
            else:
                proyectos.append(id)
                dias.append(dia)
                al.append(0)

    diccionario = {'IdProy': proyectos ,'Dia': dias, 'Alarma': al}
    df = pd.DataFrame(diccionario)
    # Pivotar la tabla
    pivot = df.pivot(index='IdProy', columns='Dia', values='Alarma').reset_index()
    pivot

def informedia():
    # Obtener la fecha actual
    hoy = datetime.date.today()
    # Calcular el día de ayer
    ayer = hoy - datetime.timedelta(days=1)

    DIA_MAX = ayer.day

    alarmas = alarmasfact()
    alarmas = alarmas[ alarmas['diai'] == DIA_MAX ]
    idproy = alarmas['IdProy'].unique()

    proyectos=[]
    dias = []
    al=[]

    for id in idproy:
        for dia in range(1,DIA_MAX+1):
            temp = alarmas[(alarmas['IdProy'] == id) & (alarmas['diai'] == dia)]
            if not temp.empty:
                proyectos.append(id)
                dias.append(dia)
                al.append(1)

    diccionario = {'IdProy': proyectos ,'Dia': dias, 'Alarma': al}
    df = pd.DataFrame(diccionario)
    # Pivotar la tabla
    pivot = df.pivot(index='IdProy', columns='Dia', values='Alarma').reset_index()
    pivot

