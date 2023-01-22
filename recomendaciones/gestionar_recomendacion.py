
''' RIX BOT  ---- GESTIÓN DE RECOMENDACIONES '''

############################################################################
######################### LIBRERÍAS ########################################

import pandas as pd                     # Pandas
from datetime import datetime as d_t    # Librería Datetime
import pytz as tz                       # Librería TimeZones
import json
import os
import matplotlib.pyplot as plt
import statistics as stats
import sklearn
from sklearn.neighbors import NearestNeighbors
import numpy as np

###################################################################################
####################### CARGAR DATOS DE BODEGA ####################################

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

# 3 Generar imagen de respuesta

def df_to_image(df):

    title_text = 'Consulta en Bodega'
    fecha = time_in_pty()
    fig_background_color = 'skyblue'
    fig_border = 'steelblue'
    data = df
    
    archivo = fecha+"consulta.png"              #Almacenamiento
    
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

########################################################################################
####################### FUNCIÓN DE BUSQUEDA DIRECTA ####################################

def busqueda_directa(texto):
    bodega_json = abrir_json('')
    
#######################################################################################
#################################### RECOMENDACIÓN ####################################

# 1 Transformar datos de entrada 

def get_df_raw(raw_text):
  df = pd.DataFrame(raw_text,columns=['text'], index=['año','potencia','rango_precio','consumo','combustible','plazas','transmisión'])
  return df

try_it = ['año del auto: 2019', '235 caballos de fuerza', '27900 dólares', '40 millas por galón', 'gasolina', '4 asientos', 'automática']
df_1 = get_df_raw(try_it)
df_1

# 2 Asignación de 

def ajustar_df(bodega_raw):
    df_bodega = bodega_raw.copy()
    df_bodega["tipo"].replace(["gasolina","diesel","electrico", "hibrido"],[0,1,2,3],inplace=True)
    df_bodega["transmicion"].replace(["automatico","manual"],[0,1],inplace=True)
    promedio =[]
    for rango in df_bodega["rango_de_precio"]:
      prom = stats.mean(rango)
      promedio.append(prom)
    df_bodega.drop(["rango_de_precio"],axis=1,inplace=True)
    df_bodega.insert(3,"promedio_precio",promedio)
    return df_bodega
# 3 KNN Modelo FIT de recomendación

def recomendar_busqueda_df(m:list,df):

    #['año','potencia','rango_precio','consumo','combustible','plazas','transmisión']
    datos_recomendar = df.iloc[:,[1,2,3,4,5,6,7]].values
    nn = NearestNeighbors(n_neighbors=1).fit(x)
    y = nn.kneighbors([m])
    auto = y[1][0][0]
    recomend = pd.DataFrame(df.iloc[auto])
    return recomend

'''m = [2020,120,15500,30,1,3,0]  
prt=recomendar_busqueda_df(m,df_bodega1)
prt'''



######################################################################
# ========================== MAIN ====================================

time_in_pty()

bodega_json = abrir_json('bodega_autos.json')
print(bodega_json)

autos = json_to_multidf(bodega_json)
print(autos)

usuario = ['camioneta', 'toyota']

auto = buscar_bodega(usuario,autos)
print(auto)


printable_df = preparar_respuesta_busqueda(auto)
print(printable_df)


p = df_to_image(auto)
print(p)
