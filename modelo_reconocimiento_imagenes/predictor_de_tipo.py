
# ==================== LIBRERÍAS ==========================
from tensorflow.keras.models import load_model
import tensorflow_hub as hub
import numpy as np
from PIL import Image
import requests
from io import BytesIO
import cv2
# ===================== FUNCIÓN ==========================
def cargar_modelo(ruta):
    # Recrea exactamente el mismo modelo solo desde el archivo
    modelo = load_model(r'C:\Users\HP-LAPTOP\Documents\GitHub\chat_bot\modelo_reconocimiento_imagenes\modelo_carros.h5',custom_objects={'KerasLayer': hub.KerasLayer})
    return modelo

def categorizar(url,ruta):
    modelo = cargar_modelo(ruta)
    respuesta = requests.get(url)
    img = Image.open(BytesIO(respuesta.content))
    img = np.array(img).astype(float)/255

    img = cv2.resize(img, (224,224))
    prediccion = modelo.predict(img.reshape(-1, 224, 224, 3))
    return np.argmax(prediccion[0], axis=-1)

def hacer_prediccion(url):
  prediccion = categorizar(url,r'C:\Users\HP-LAPTOP\Documents\GitHub\chat_bot\modelo_reconocimiento_imagenes\modelo_carros.h5')
  print(prediccion)
  return prediccion

'''Casos'''
# 0 camionetas
# 1 coupe
# 2 deportivos
# 3 pick up
# 4 sedan

#######################################################################
##############################  MAIN  #################################

'''
if __name__ == '__main__':

    prediccion = hacer_prediccion(user_url)
'''   
