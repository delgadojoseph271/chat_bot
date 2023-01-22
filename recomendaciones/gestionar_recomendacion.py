
''' RIX BOT  ---- GESTIÓN DE RECOMENDACIONES '''

############################################################################
######################### LIBRERÍAS ########################################

import pandas as pd                     # Pandas
from datetime import datetime as d_t    # Librería Datetime
import pytz as tz                       # Librería TimeZones
import json
import os
import matplotlib.pyplot as plt
import numpy as np
import sys
# ------------------------------

sys.path.append(r'C:\Users\HP-LAPTOP\Documents\GitHub\chat_bot\procesamiento_caracteristicas')
sys.path.append(r'C:\Users\HP-LAPTOP\Documents\GitHub\chat_bot\modelo_reconocimiento_imagenes')

path = r'C:\Users\HP-LAPTOP\Documents\GitHub\chat_bot\gestion_bodega\bodega_autos.json'

import spacy_procesador_texto as spt
import predictor_de_tipo as pdt

###################################################################################
####################### FUNCIONES GENERALES ####################################

# 0 Fecha y hora local
def time_in_pty():
    time_zone = "America/Panama"                        # Configura la región y el nombre de la zona horaria
    pty = tz.timezone(time_zone)                        # Busca la zona horaria
    date_pty = d_t.now(pty)                             # Obtiene la hora en la zona horaria dada
    f_date_pty = date_pty.strftime("%m_%d__%H_%M")      # Configuración del formato de Fecha, Hora y Zona horaria
    return f_date_pty                                   # Hora de Ejecución


# 1 Asignar para abrir bodega para recomendación
def abrir_json(ruta:str):
    data_file= open(ruta).read()                        # Cargar el archivo en formato json
    intents = json.loads(data_file)                     # Convertir el archivo json a diccionario
    return intents

# 2 Creación de un DF multi índice
def json_to_multidf(dataframe):
    multi_df = pd.concat({k:pd.DataFrame(v).T for k, v in dataframe.items()},axis=0)
    return multi_df

# 3 Generar imagen de respuesta

def df_to_image(df,tipo):

    title_text = 'Consulta en Bodega'
    fecha = time_in_pty()
    fig_background_color = 'skyblue'
    fig_border = 'steelblue'
    data = df
    
    archivo = f'C:/Users/HP-LAPTOP/Documents/GitHub/chat_bot/recomendaciones/consultas/Consulta_{tipo}_{fecha}.png'              #Almacenamiento
    
    column_headers = data.columns               # Nombre de las columnas de la tabla
    row_headers = [x for x in data.index]       # Nombre de las filas de la tabla

    cell_text = []
    for row in data.values:                     # Información de la tabla
        cell_text.append(row)

    # Get some lists of color specs for row and column headers
    rcolors = plt.cm.BuPu(np.full(len(row_headers), 0.1))
    ccolors = plt.cm.BuPu(np.full(len(column_headers), 0.1))

    # Create the figure. Setting a small pad on tight_layout
    # seems to better regulate white space. Sometimes experimenting
    # with an explicit figsize here can produce better outcome.
    plt.figure(linewidth=2,
            edgecolor=fig_border,
            facecolor=fig_background_color,
            tight_layout={'pad':1},
            #figsize=(5,3)
            )

    # Add a table at the bottom of the axes
    the_table = plt.table(cellText=cell_text,
                        rowLabels=row_headers,
                        rowColours=rcolors,
                        rowLoc='right',
                        colColours=ccolors,
                        colLabels=column_headers,
                        loc='center')

    # Ajuste del tamaño de las filas (i.e., make cell y scale larger).
    the_table.scale(1, 1.5)

    # Quitar ejes
    ax = plt.gca()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    # Quitar borde de ejes
    plt.box(on=None)

    # Agregar título
    plt.suptitle(title_text)

    # Agregar Pie de foto
    plt.figtext(0.95, 0.05, fecha, horizontalalignment='right', size=6, weight='light')

    # Fuerza la actualización de la figura, para que los backends centren los objetos correctamente dentro de la figura.
    # Sin plt.draw() aquí, el título se centrará en los ejes y no en la figura.
    plt.draw()

    # Crear imagen. plt.savefig ignora los colores de borde y cara de la figura, así que mapealos.
    fig = plt.gcf()
    plt.savefig(archivo,
              edgecolor=fig.get_edgecolor(),
              facecolor=fig.get_facecolor(),
              dpi=150
              )
  
    return archivo

#############################################################################
####################### BUSQUEDA DIRECTA ####################################

# 1 Busqueda directa en bodega

def buscar_bodega(datos,df):
    car_serie = pd.DataFrame(df.loc[datos[0]].loc[datos[1]])
    return car_serie

# 2 Preparar respuesta de busqueda

def preparar_respuesta_busqueda(df):
    df.index = ['Modelo', 'Año', 'Potencia', 'Rango de precio (US Dolar)', 'Consumo de combustible',
       'Tipo de Combustible', 'Plazas', 'Transmisión']
    df.columns=[df.columns[0].title()]
    df.replace()
    return df


######################################################################
# ========================== MAIN ====================================

bodega_json = abrir_json(path)

df_bodega = json_to_multidf(bodega_json)


########################################################################################
####################### FUNCIÓN DE BUSQUEDA DIRECTA ####################################

def busqueda_directa(texto:list):
    auto = buscar_bodega(texto,df_bodega)
    datos = preparar_respuesta_busqueda(auto)
    resultado = df_to_image(datos,"direct")
    print(f'Salida: {resultado}')
    return resultado
    
    
################################################################################################
####################### FUNCIÓN DE BUSQUEDA CARACTERÍSTICAS ####################################

def busqueda_caracteristicas(entrada):
    auto = spt.recomendacion_caracteristicas(entrada, df_bodega)
    resultado = df_to_image(auto,"recomend")
    print(f'Salida: {resultado}')
    return resultado

################################################################################################
####################### FUNCIÓN DE BUSQUEDA URL ####################################
''' FUNCIÓN BETA '''

def referencia_url(entrada:int,df):
  tipo = entrada
  nt=[]
  if tipo == 4:
    nt.append("sedán")
  elif tipo == 3:
    nt.append('pickup')
  elif tipo == 2 :
    nt.append('deportivo')
  elif tipo == 0:
    nt.append('camioneta')
  elif tipo == 1:
    nt.append('coupé')
  print(nt)
  df.columns = ["Modelo","Año","Potencia(HP)","Rango de Precios","Consumo de combustible","Tipo de combustible","N° Asientos","Transmision"]
  df_resultado = pd.DataFrame(df.loc[nt[0]])
  return df_resultado

def busqueda_url(url):
    entrada = pdt.hacer_prediccion(url)
    auto = referencia_url(entrada,df_bodega)
    resultado = df_to_image(auto,"url")
    print(f'Salida: {resultado}')
    return resultado
    
# PRUEBAS

'''usuario = ['sedán', 'nissan']
busqueda_directa(usuario, df_bodega)

try_it = ['año del auto: 2019', '235 caballos de fuerza', '27900 dólares', '40 millas por galón', 'gasolina', '4 asientos', 'automática']
busqueda_caracteristicas(try_it,df_bodega)'''

#busqueda_url("https://www.nissan-cdn.net/content/dam/Nissan/mexico/vehicles/NP300/my21/vlp/np300-2021_blanca-exterior-piloto.jpg.ximg.l_full_h.smart.jpg")
