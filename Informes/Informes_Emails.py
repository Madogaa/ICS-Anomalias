# %%
import os
os.chdir(r'C:\\Users\\mario\\OneDrive\\Documentos\\ICS Anomalías\\Códigos_Análisis')

import pandas as pd
from Alarmas.Alarmas_Proy_Dia_Cuad import*
from Datos.Base_datos import*
import smtplib
import calendar
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tabulate import tabulate
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def enviar_email(destinatario, asunto, mensaje):
    # Configurar los detalles del servidor de correo
    servidor_smtp = 'smtp-mail.outlook.com'
    puerto_smtp = 587
    remitente = 'mariogarcia@icsred.com'
    contraseña = ''

    # Crear el mensaje MIME
    mensaje_mime = MIMEMultipart('alternative')
    mensaje_mime['From'] = remitente
    mensaje_mime['To'] = destinatario
    mensaje_mime['Subject'] = asunto

    # Crear la parte HTML del mensaje
    mensaje_html = MIMEText(mensaje, 'html')

    mensaje_mime.attach(mensaje_html)

    try:
        # Establecer una conexión segura con el servidor SMTP
        servidor = smtplib.SMTP(servidor_smtp, puerto_smtp)
        servidor.starttls()
        servidor.login(remitente, contraseña)

        # Enviar el correo electrónico
        servidor.sendmail(remitente, destinatario, mensaje_mime.as_string())

        print('Correo electrónico enviado correctamente.')
    except Exception as e:
        print('Error al enviar el correo electrónico:', str(e))
    finally:
        servidor.quit()

def enviar_informe(dia,mes,año,alarmas):
    DIA = dia
    alarmas = alarmas[(~alarmas['alarma'].isnull()) & (alarmas['diai'] == DIA)]
    if(alarmas.empty):
        return f'No hay alarmas para la fecha: {dia}-{mes}-{año}'
    MES_NORM = (mes - 12 * (año-2021))
    alarmas['IdProy'] = alarmas['IdProy'].astype(int)
    alarmas = alarmas.round(2)
    # Header informe
    mensaje = '<h2>Dia del informe: ' + str(DIA) + '</h2>'
    mensaje += '<h2>Mes del informe: ' + calendar.month_name[MES_NORM] + '</h2>'
    mensaje += '<h3>Ultima actualizacion BBDD: ' + act_date(Filtro()) + '</h3>'
    # Convertir el DataFrame en una tabla HTML con estilos en línea
    tabla_html = alarmas.to_html(index=False, justify='center', classes='data', border=0, table_id='tabla')
    # Agregar estilos en línea para la tabla
    tabla_html = tabla_html.replace('<table', '<table style="border: 3px solid #002d72; border-radius: 8px;"')
    tabla_html = tabla_html.replace('<th', '<th style="background-color: #002d72; color: white; padding: 8px;"')
    tabla_html = tabla_html.replace('<td', '<td style="padding: 8px; border: 3px solid #002d72; border-radius: 10px;"')
    # Crear objeto BeautifulSoup
    soup = BeautifulSoup(tabla_html, 'html.parser')
    # Encontrar todas las etiquetas <tr>
    tbody = soup.find('tbody')
    filas = tbody.find_all('tr')
    # Agregar la tabla al mensaje
    for i, fila in enumerate(filas):
        if (i+1) % 2 == 0:  # Filas pares
            fila['style'] = 'background-color: #cce5ff; text-align: center;'
        else:  # Filas impares
            fila['style'] = 'text-align: center;'

    # Ejemplo de uso
    destinatario = 'alumno.38254@ies-azarquiel.es'
    asunto = f'Anomalias Facturacion Diaria {dia}-{mes}-{año}'
    mensaje += soup.prettify()
    enviar_email(destinatario, asunto, mensaje)

fecha = datetime.now() - timedelta(days=1)
dia = fecha.day
mes = fecha.month
anio = fecha.year
enviar_informe(dia,mes,anio,alarmasdiavta(dia,mes))
# %%
