from time import sleep # Tiempos de Espera
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
import re # Limpieza de Datos. Expresiones regulares.
from unicodedata import normalize #Normaliza caracteres del Español
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

''' ----------------- GESTIÓN DE SESIÓN EN LINEA ----------------- '''

ruta_archivo = "./whatsapp_session.txt" #Archivo de Sesión guardado en la misma carpeta que el resto del proyecto
driver = webdriver

def crear_driver_session():
    #ABrir archivo de Sesión
    with open(ruta_archivo) as fp:
        for cnt, line in enumerate(fp):
            if cnt == 0:
                 executor_url = line
            if cnt == 1:
                session_id = line

    def new_command_execute(self, command, params=None):
        if command == "newSession":
            
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return org_command_execute(self, command, params)
                
    org_command_execute = RemoteWebDriver.execute

    RemoteWebDriver.execute = new_command_execute

    new_driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
    new_driver.session_id = session_id

    RemoteWebDriver.execute = org_command_execute

    return new_driver
 
''' -------------- SELECCIÓN Y PREPARACIÓN DEL MENSAJE -------------- '''

def normalizar(mensaje: str):
    # Elimina tildes y normaliza el texto para evitar problemas
    mensaje = re.sub(
        r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
        normalize( "NFD", mensaje), 0, re.I
    )

    # -> NFC
    return normalize( 'NFC', mensaje)

# IMPORTANTE!!!!
#Requiere de constante actualización/revisión en la sección CLASS_NAME
def identificar_mensajes():
    element_box_message = driver.find_elements(By.CLASS_NAME,"_27K43") # todos los cuadritos de mensajes 
    #print("mensajes:", element_box_message)
    posicion = len(element_box_message) -1

    element_message = element_box_message[posicion].find_elements(By.CLASS_NAME,"_21Ahp") #  Texto msj entrante Whatsapp
    #print("mensaje:" ,element_message)

    mensaje = element_message[0].text.lower().strip()
    print("MENSAJE RECIBIDO :", mensaje)
    return normalizar(mensaje)

def verificar_mensajes_pendientes(chat):
    '''Funcion para verificar si existen mensajes por leer,
    en algunos casos la class=_1pJ9J, no se consigue,
    por eso se agrego la exception, y retorna verdadero (True) 
    si el bloque que se esta verificando tiene mensajes sin leer'''
    try:
        icono_mensajes = chat.find_element(By.CLASS_NAME,"_1pJ9J").text                
        
        msj_leer = re.findall('\d+' ,icono_mensajes)        
        
        if len(msj_leer) != 0:
            pendiente = True
             
        else:
            # Usuarios silenciados, el simbolo posee el mismo nombre de la clase pero no
            #contiene decimales
            pendiente = False
        
    except:        
        pendiente = False
    return pendiente


''' ----------------- BUSQUEDA E INTERACCIÓN ----------------- '''

def buscar_chats():
    print("BUSCANDO CHATS")
    sleep(5)
    
    '''Pruebas'''
    #print("Elemento encontrado:" ,driver.find_element(By.CLASS_NAME,"_1RAKT"))
    #print(len(driver.find_elements(By.CLASS_NAME,"_1RAKT")))# si la longitud es 0 es porque tengo chat abierto, si es dif de 0 es porque  no hay chat abierto

    if len(driver.find_elements(By.CLASS_NAME,"zaKsw")) == 0:
        # Cuando ninguno esta abierto (ventana de la derecha)
        
        print("CONVERSACIÓN ABIERTA")
        mensaje = identificar_mensajes()
                                
        if mensaje != None: # Control de Casos donde no es un mensaje
            return True 
    else:
        
        chats = driver.find_elements(By.CLASS_NAME,"_1Oe6M")
        # El cuadro del primer chat a la izquierda
                
        print("Lista de chats: ",len(chats))
        for chat in chats:
            print("DETECTANDO MENSAJES SIN LEER")
            chat_mensajes = chat.find_elements(By.CLASS_NAME,"_1pJ9J")
            
            if len(chat_mensajes) == 0:
                print("CHATS ATENDIDOS")
                continue
            
            else:
                chat.click() # Abre el chat
                return True

            
            por_responder = verificar_mensajes_pendientes(chat) # Verificar si existen mensajes por leer
            
            # Condicion para entrar en cada conversacion (Solo entra si existen mensajes sin leer)
            if por_responder:
                # Si existen mensajes sin responder debemos dar click sobre ese chat.            
                chat.click()  # Se da click sobre la conversacion.
                sleep(2)
                return True
            else:
                print("CHATS ATENDIDOS")
                continue                
    return False


def preparar_respuesta(mensaje :str):
    print("PREPARANDO RESPUESTA")

    '''if mensaje.__contains__("hola"): # Equivalente a if message=="hola"
        respuesta = 'Hola\nSoy Un Bot\nPrueba Exitosas'
    elif mensaje.__contains__("gracias"):
        respuesta = "Ha sido un placer"
    else:        
        respuesta = "Mensaje no identificado"'''

    '''Caso Final'''
    respuesta=bot(mensaje)

    return respuesta

def procesar_mensaje(mensaje :str):
    
    chat_box = driver.find_element(By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p')
    # Se copia el path de la caja de texto donde se escribe
    # En este caso xpath en vez de class porque no reconocia el class        
    respuesta = preparar_respuesta(mensaje) # AQUI CONECTAMOS CON EL CHATBOT
    print("Respuesta: ",respuesta)

        
    chat_box.send_keys(respuesta, Keys.ENTER)
    sleep(2)
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    # Generar ESC para salir de la conversacion

''' ----------------- INICIAR DE SESIÓN EN LINEA ----------------- '''

def whatsapp_bot_init():
    global driver
    driver = crear_driver_session()

    esperando=1
    
    while esperando== 1:
        esperando=len(driver.find_elements(By.CLASS_NAME,"_1N3oL"))
        sleep(15) # Aquí también depende del tiempo de arranque del navegador. No es muy práctico pero es funcional.
        print("login_sucess: ", esperando)
        
    while True:
        if not buscar_chats(): # Busca si hay chats, y si tienen mensajes sin leer
            sleep(5)
            continue
        
        msj_recibido = identificar_mensajes()

        if msj_recibido == None:
            continue
        else:
            procesar_mensaje(msj_recibido)

'''//////////////////////////////////////////////// MAIN ////////////////////////////////////////////////'''
# Controlador

from sesion_activa import iniciar_mantener_sesion
from chatbot import bot

if __name__ == '__main__':
    iniciar_mantener_sesion()
    sleep(8) #Verificar Tiempo de Espera. Depende de la rapidez de la laptop.
    whatsapp_bot_init()

