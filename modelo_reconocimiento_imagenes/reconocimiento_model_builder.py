# ============================= LIBRERÍAS =================================
import os
import shutil as sh

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np

import tensorflow as tf
import tensorflow_hub as hub

# ============================= CREACIÓN DE CARPETAS =================================

'''SOLO EJECUTAR LA PRIMERA VEZ'''

'''
# Carpeta coupe raw
os.mkdir(r'.\coupes')

# Carpeta deportivos raw
os.mkdir(r'.\deportivos')

# Carpeta sedanes raw
os.mkdir(r'.\sedanes')

# Carpeta camionetas raw
os.mkdir(r'.\camionetas')

# Carpeta pickups raw
os.mkdir(r'.\pickups')
'''

#================================== UNZIP FILES ====================================
'''SOLO EJECUTAR LA PRIMERA VEZ'''
# Se debe agregar el path local del dispositivo donde se ejecutará el modelo

#os.chdir(r'C:\Users\ruta_archivoz_zip\zip') # Carpeta donde están los archivos zip
#sh.unpack_archive('coupes.zip', r'C:\Users\...\carpeta_de_ubicacion\coupes')
#sh.unpack_archive('deportivos.zip', r'C:\Users\...\carpeta_de_ubicacion\deportivos')
#sh.unpack_archive('sedanes.zip', r'C:\Users\...\carpeta_de_ubicacion\sedanes')
#sh.unpack_archive('camionetas.zip', r'C:\Users\...\carpeta_de_ubicacion\camionetas')
#sh.unpack_archive('pickups.zip', r'C:\Users\...\carpeta_de_ubicacion\pickups')
#os.chdir(r'C:\Users\...\carpeta_de_ubicacion\carpeta_raiz')
print("Unzip listo")

#=================================================================================

# Rutas Origen

'''coupes_o = r'.\coupes'
deportivos_o = r'.\deportivos'
sedanes_o = r'.\sedanes'
camionetas_o = r'.\camionetas'
pickups_o = r'.\pickups'''

'''# Cantidad de datos

n_coupes_o = os.listdir(coupes_o)
print(f' Total de  Coupes: {len(n_coupes_o)}')

n_deportivos_o = os.listdir(deportivos_o)
print(f' Total de  Deportivos: {len(n_deportivos_o)}')

n_sedanes_o = os.listdir(sedanes_o)
print(f' Total de  Sedanes: {len(n_sedanes_o)}')

n_camionetas_o = os.listdir(camionetas_o)
print(f' Total de  Camionetas: {len(n_camionetas_o)}')

n_pickups_o = os.listdir(pickups_o)
print(f' Total de  Pickups: {len(n_pickups_o)}')'''



#================================== DATASETS ===============================================
'''SOLO EJECUTAR LA PRIMERA VEZ'''
'''
os.mkdir(r'.\datasets')

# Carpeta coupe
os.mkdir(r'.\datasets\coupes')

# Carpeta deportivos
os.mkdir(r'.\datasets\deportivos')

# Carpeta sedanes
os.mkdir(r'.\datasets\sedanes')

# Carpeta camionetas
os.mkdir(r'.\datasets\camionetas')

# Carpeta pickups
os.mkdir(r'.\datasets\pickups')
'''

# Rutas datasets
coupes_d = r'.\datasets\coupes'
deportivos_d = r'.\datasets\deportivos'
sedanes_d = r'.\datasets\sedanes'
camionetas_d = r'.\datasets\camionetas'
pickups_d = r'.\datasets\pickups'
# Número de Datos

n_coupes_d = os.listdir(r'.\datasets\coupes')
n_deportivos_d = os.listdir(r'.\datasets\deportivos')
n_sedanes_d = os.listdir(r'.\datasets\sedanes')
n_camionetas_d = os.listdir(r'.\datasets\camionetas')
n_pickups_d = os.listdir(r'.\datasets\pickups')


print(f' Total de  Coupes: {len(n_coupes_d)}')
print(f' Total de  Deportivos: {len(n_deportivos_d)}')
print(f' Total de  Sedanes: {len(n_sedanes_d)}')
print(f' Total de  Camionetas: {len(n_camionetas_d)}')
print(f' Total de  Pickups: {len(n_pickups_d)}')

def crear_copia(fuente,destino):
    carpeta_fuente = fuente
    carpeta_destino = destino
    
    imagenes = os.listdir(carpeta_fuente)

    for i, nombreimg in enumerate(imagenes):
      if i < len(imagenes):
        #Copia de la carpeta fuente a la destino
        sh.copy(carpeta_fuente + '/' + nombreimg, carpeta_destino + '/' + nombreimg)

'''
crear_copia(coupes_o , coupes_d)
crear_copia(deportivos_o , deportivos_d)
crear_copia(sedanes_o , sedanes_d)
crear_copia(camionetas_o , camionetas_d)
crear_copia(pickups_o , pickups_d)
'''

print("Copias Listas")

#============================== CONSTRUCTOR DE MODELO =======================================

#Crear el dataset generador
datagen = ImageDataGenerator(
    rescale=1. / 255,
    rotation_range = 30,
    width_shift_range = 0.25,
    height_shift_range = 0.25,
    shear_range = 15,
    zoom_range = [0.5, 1.5],
    validation_split=0.2 #20% para pruebas
)

#Generadores para sets de entrenamiento y pruebas
data_gen_entrenamiento = datagen.flow_from_directory('./datasets', target_size=(224,224),
                                                     batch_size=32, shuffle=True, subset='training')
data_gen_pruebas = datagen.flow_from_directory('./datasets', target_size=(224,224),
                                                     batch_size=32, shuffle=True, subset='validation')

#Imprimir 10 imagenes del generador de entrenamiento
for imagen, etiqueta in data_gen_entrenamiento:
  for i in range(10):
    plt.subplot(2,5,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.imshow(imagen[i])
  break
plt.show()

#==============================================================================

url = "https://tfhub.dev/google/tf2-preview/mobilenet_v2/feature_vector/4"
mobilenetv2 = hub.KerasLayer(url, input_shape=(224,224,3))

#Congelar el modelo descargado
mobilenetv2.trainable = False

#
modelo = tf.keras.Sequential([
    mobilenetv2,
    tf.keras.layers.Dense(5, activation='softmax')
])

#
modelo.summary()


#Compilar como siempre

modelo.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

#Entrenar el modelo

EPOCAS = 50

historial = modelo.fit(
    data_gen_entrenamiento, epochs=EPOCAS, batch_size=32,
    validation_data=data_gen_pruebas
)

#=========================================================================
#Graficas de precisión
acc = historial.history['accuracy']
val_acc = historial.history['val_accuracy']

loss = historial.history['loss']
val_loss = historial.history['val_loss']

rango_epocas = range(50)

plt.figure(figsize=(8,8))
plt.subplot(1,2,1)
plt.plot(rango_epocas, acc, label='Precisión Entrenamiento')
plt.plot(rango_epocas, val_acc, label='Precisión Pruebas')
plt.legend(loc='lower right')
plt.title('Precisión de entrenamiento y pruebas')

plt.subplot(1,2,2)
plt.plot(rango_epocas, loss, label='Pérdida de entrenamiento')
plt.plot(rango_epocas, val_loss, label='Pérdida de pruebas')
plt.legend(loc='upper right')
plt.title('Pérdida de entrenamiento y pruebas')
plt.show()

modelo.save('./modelo_carros.h5',historial)
