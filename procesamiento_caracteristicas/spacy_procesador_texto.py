# ESTE DOCUMENTO ESTÁ CONDICINADO A LAS CONDICIONES DE LA BODEGA
# CUALQUIER EJECUCIÓN CON OTROS DATOS GENERARÁ ERRORES

########################## LIBRERÍAS #########################################3

import spacy
from spacy.matcher import Matcher
import es_core_news_sm
import statistics as stats
import sklearn
from sklearn.neighbors import NearestNeighbors
import pandas as pd

'''--------------------- PROCESAMIENTO DE DATOS ---------------------'''

# Pendiente de implementar clases

#1 PROCESAR AÑO

def get_year(df):
  dato = df.loc["año"][0]
  nlp = spacy.load('es_core_news_sm')
  doc = nlp(dato)
  print(doc)
  pattern2 =  [{"LIKE_NUM": True}]

  matcher = Matcher(nlp.vocab) 
  matcher.add("dato", [pattern2])
  matches = matcher(doc)
  print(matches)

  for match_id, start, end in matches:
    # Obtén el span resultante
    matched_span = doc[start:end]
   
    year = matched_span.text
    return int(year)

#2 PROCESAR POTENCIA

def get_potencia(df):
  dato = df.loc["potencia"][0]

  nlp = spacy.load('es_core_news_sm')
  doc = nlp(dato)
  print(doc)
  pattern2 =  [{"LIKE_NUM": True}]

  matcher = Matcher(nlp.vocab) 
  matcher.add("dato", [pattern2])
  matches = matcher(doc)
  print(matches)

  for match_id, start, end in matches:
    # Obtén el span resultante
    matched_span = doc[start:end]
   
    potencia = matched_span.text
    return int(potencia)

#3 PROCESAR PRECIO APROXIMADO

def get_precio_promedio(df):
  dato = df.loc["rango_precio"][0]
  
  nlp = spacy.load('es_core_news_sm')
  doc = nlp(dato)
  print(doc)
  pattern2 =  [{"LIKE_NUM": True}]

  matcher = Matcher(nlp.vocab) 
  matcher.add("dato", [pattern2])
  matches = matcher(doc)
  print(matches)

  for match_id, start, end in matches:
    # Obtén el span resultante
    matched_span = doc[start:end]
   
    precio_promedio = matched_span.text
    return float(precio_promedio)


#4 PROCESAR CONSUMO

def get_consumo(df):
  dato = df.loc["consumo"][0]
  
  nlp = spacy.load('es_core_news_sm')
  doc = nlp(dato)
  print(doc)
  pattern2 =  [{"LIKE_NUM": True}]

  matcher = Matcher(nlp.vocab) 
  matcher.add("dato", [pattern2])
  matches = matcher(doc)
  print(matches)

  for match_id, start, end in matches:
    # Obtén el span resultante
    matched_span = doc[start:end]
   
    consumo = matched_span.text
    return int(consumo)

#5 PROCESAR TIPO DE COMBUSTIBLE
 
def  combustible_value(tipo):
  casos = ["gasolina","diesel","eléctrico", "híbrido"]
  value = [0,1,2,3]
  
  # Gasolina value
  if tipo in casos[0]:
    return value[0]
  # Diesel
  elif tipo in casos[1]:
    return value[1]
  # Eléctrico
  elif tipo in casos[2]:
    return value[2]
  elif tipo in casos[3]:
    return value[3]

def get_combustible(df):
  dato = df.loc["combustible"][0]

  nlp = spacy.load('es_core_news_sm')
  doc = nlp(dato)
  print(doc)
  pattern1 =  [{'LOWER' : {'IN' : ["gasolina","diesel","eléctrico","electrico","hibrido","híbrido"]}}]
  
  matcher = Matcher(nlp.vocab) 
  matcher.add("dato", [pattern1])
  matches = matcher(doc)
  print(matches)

  for match_id, start, end in matches:
    # Obtén el span resultante
    matched_span = doc[start:end]
   
    combustible = matched_span.text
    df_value = combustible_value(combustible)
    return int(df_value)


# 6 PROCESAR NÚMERO DE ASIENTOS

def get_asientos(df):
  dato = df.loc["plazas"][0] 

  nlp = spacy.load('es_core_news_sm')
  doc = nlp(dato)
  print(doc)
  pattern2 =  [{"LIKE_NUM": True}]

  matcher = Matcher(nlp.vocab) 
  matcher.add("dato", [pattern2])
  matches = matcher(doc)
  print(matches)

  for match_id, start, end in matches:
    # Obtén el span resultante
    matched_span = doc[start:end]
   
    asientos = matched_span.text
    return int(asientos)

# 7 PROCESAR TRANSMISIÓN

def get_transmision_value(tipo):
  casos = ["manual","automática","automatica"]
  value = [0,1,1]
  
  # Transmisión value
  # manual
  if tipo in casos[0]:
    return value[0]
  # automática
  elif tipo in casos[1]:
    return value[1]
  elif tipo in casos[2]:
    return value[1]

def get_transmision(df):
  dato = df.loc["transmisión"][0]

  nlp = spacy.load('es_core_news_sm')
  doc = nlp(dato)
  print(doc)
  pattern1 =  [{'LOWER' : {'IN' : ["manual","automatica","automática"]}}]
  
  matcher = Matcher(nlp.vocab) 
  matcher.add("dato", [pattern1])
  matches = matcher(doc)
  print(matches)

  for match_id, start, end in matches:
    # Obtén el span resultante
    matched_span = doc[start:end]
   
    tipo = matched_span.text
    transmision = get_transmision_value(tipo)
    return int(transmision)

##################################### METODOS PRINCIPALES ############################################

# 1 Transformar datos de entrada 

def get_df_raw(raw_text):
  df = pd.DataFrame(raw_text,columns=['text'], index=['año','potencia','rango_precio','consumo','combustible','plazas','transmisión'])
  return df

# 2 Obtención de data ajustada

def get_data_user(df):

    lista_features = [get_year(df),get_potencia(df),get_precio_promedio(df),
                      get_consumo(df),get_combustible(df),get_asientos(df),
                      get_transmision(df)]
    print(f"Datos de recomendación: {lista_features}")
    return lista_features

# 3 Asignación de datos de Bodega ajustados

def ajustar_df(bodega_raw):
    print(bodega_raw)
    df_bodega = bodega_raw.copy()
    df_bodega["tipo"].replace(["gasolina","diesel","electrico", "hibrido"],[0,1,2,3],inplace=True)
    df_bodega["transmision"].replace(["automatico","manual"],[0,1],inplace=True)
    promedio =[]
    for rango in df_bodega["rango_de_precio"]:
      prom = stats.mean(rango)
      promedio.append(prom)
    df_bodega.drop(["rango_de_precio"],axis=1,inplace=True)
    df_bodega.insert(3,"promedio_precio",promedio)

    return df_bodega

# 4 KNN Modelo FIT de recomendación

def recomendar_busqueda_df(m:list,df):
    #['año','potencia','rango_precio','consumo','combustible','plazas','transmisión']
    datos_recomendar = df.iloc[:,[1,2,3,4,5,6,7]].values
    print(datos_recomendar)
    nn = NearestNeighbors(n_neighbors=1).fit(datos_recomendar)
    y = nn.kneighbors([m])
    auto = y[1][0][0]
    recomend = pd.DataFrame(df.iloc[auto])
    return recomend


#####################################################################################################
############################################# MAIN ##################################################


def recomendacion_caracteristicas(entrada, bodega):
   df_datos = get_df_raw(entrada)
   ajuste_bodega = ajustar_df(bodega)
   features = get_data_user(df_datos)

   resultado = recomendar_busqueda_df(features, ajuste_bodega)
   return resultado

#----------------------------------------------------------------------------------------------------

'''if __name__ == '__chatbot__':

  recomendacion = recomendacion_caracteristicas(entrada, bodega):'''



  




