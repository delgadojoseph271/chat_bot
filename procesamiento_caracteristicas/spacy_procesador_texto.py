# ESTE DOCUMENTO ESTÁ CONDICINADO A LAS CONDICIONES DE LA BODEGA
# CUALQUIER EJECUCIÓN CON OTROS DATOS GENERARÁ ERRORES

########################## LIBRERÍAS #########################################3

import spacy
from spacy.matcher import Matcher
import es_core_news_sm
  
'''--------------------- PROCESAMIENTO DE DATOS ---------------------'''

#1 PROCESAR AÑO

def get_year(df):
  dato = df.loc["año"][0]
  import spacy
  from spacy.matcher import Matcher
  import es_core_news_sm
  
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
    return year

#2 PROCESAR POTENCIA

def get_potencia(df):
  dato = df.loc["potencia"][0]
  import spacy
  from spacy.matcher import Matcher
  import es_core_news_sm
  
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
    return potencia

#3 PROCESAR PRECIO APROXIMADO

def get_precio_promedio(df):
  dato = df.loc["rango_precio"][0]
  import spacy
  from spacy.matcher import Matcher
  import es_core_news_sm
  
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
    return precio_promedio


#4 PROCESAR CONSUMO

def get_consumo(df):
  dato = df.loc["consumo"][0]
  import spacy
  from spacy.matcher import Matcher
  import es_core_news_sm
  
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
    return consumo

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
    return df_value

#6 PROCESAR TIPO DE COMBUSTIBLE

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
    return consumo

# PROCESAR NÚMERO DE ASIENTOS

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
    return asientos

# PROCESAR TRANSMISIÓN

def get_transmision_value(tipo):
  casos = ["manual","automatica"]
  value = [0,1]
  
  # Transmisión value
  # manual
  if tipo in casos[0]:
    return value[0]
  # automática
  elif tipo in casos[1]:
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
    trnasmision = get_transmision_value(tipo)
    return transmision

