import nltk, json,pickle
import numpy as np
import random
from nltk.stem import SnowballStemmer
from tensorflow.keras.models import load_model

tipo_marca = []
features_user = []

stemmer = SnowballStemmer('spanish')


model=load_model("chatbot_model.h5")
intents= json.loads(open("intents.json").read())
words=pickle.load(open("words.pkl","rb"))
classes=pickle.load(open("classes.pkl","rb"))


def clean_up_sentence(sentence):
    # tokenizar la oracion
    sentence_words=nltk.word_tokenize(sentence) # tokenizamos
    sentence_words=[stemmer.stem(word.lower()) for word in sentence_words] #lematizamos
    return sentence_words


def bow (sentence,words,show_details=True): #lazo entre lo que ingreso el usuario tokenizado y la referencia 
    sentence_words=clean_up_sentence(sentence)
    
    bag=[0]*len(words)
    #print("BAG TEST: ",len(bag)," : ",len(words)) # de aqui viene el problema
    for i in sentence_words:
        for j,w in enumerate(words):
            if w==i: # asigna 1 si la palabra actual está en la posición del vocabulario 
                bag[j]=1
                if show_details:
                    print("encontrado en la bolsa: ",w)
    return (np.array(bag))

# ahora si utilizo el modelo para predecir que tipo de palabra es


def predict_class(sentence,model):
    # filtrar las predicciones  por debajo del umbral
    #print("words:", len(words))
    #print("todo ok")
    #print(p)
    p = bow(sentence,words,show_details=False) # retorno del bag # p porque es el preprocesamiento
    
    res = model.predict(np.array([p]))[0] # res es la eficacia, o probabilidad de que la palabra sea de algun tipo
    #model.predict me retorna el % eficacia  , ejm 60% saludo
    # [0] es la palabra , [1] es el tag
    
    
    ERROR_THRESHOLD=0.35 #UMBRAL
    
    
    # a results le llega  [1,0,0,0]
    results= [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD] 
    # si la probabilidad es > 25% determinela como resultado correcto
    
    #r[0]= tag
    #r[1]= probabilidad
    
    #ordenar por peso de la probabilidad
    results.sort(key=lambda x: x[1], reverse=True)  
    #ordena de mayor a menor la probabilidad de que el resultado sea acertado
    return_list = []    
    for r in results:   
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})   
    print("print de return list: ", return_list)  ##  me dice de que tipo es y cual es la probabilidad de que sea correcto
    return return_list 


#Se remplazó el orden de ejecuión y los condicionales. 
#Con esto logramos incluir la RECOMENDACIÓN BASADA EN CARACTERÍSTICAS

def get_response(ints,intents_json,text): # obtiene una respuesta aleatoria segun el ints correspondiente a lo que ingreso el usuario
    global tipo_marca
    global features_user
    user_data = ["anho_del_auto", "caballos_de_fuerza", "precio_esperado", 
                  "consumo_combustible", "tipo_de_combustible", "número_de_asientos", 
                  "tipo_de_transmisión"
                ]
    tag= ints[0]["intent"] # obtenemos cual era el tag  segun lo que ingreso el usuario ints[0]
    list_of_intents=intents_json["intents"] # sacamos la lista de intents de referencia
    
    for i  in list_of_intents: 
        if (i["tag"]==tag): #miramos donde coincide el tag del sentence con la referencia
            result= random.choice(i["responses"]) # random.choice, toma un elemento aleatorio de la lista
            #if(tag=="tipo" or tag == "marca"):
              #tipo_marca.append(text)
            #if(len(tipo_marca)>1): # Esta parte Lista
              #buscar_bodega(datos)
              #print("Buscando en Bodega")
              #x = f"Funciona{tipo_marca}" # Posible funcion de busqueda
              return x
            #if(tag in user_data ):
              #features_user.append(text)
            #if(tag == "recomendar_ahora"):
              #p = f"Realizando busqueda en bodega de {features_user}" #posible función de recomendación
              #return p
            break
    return result
    
# este es el metodo principal, aqui nace todo
def chatbot_response(text): 
    ints=predict_class(text,model) 
    print(ints)
    #ints es el intents que creamos a apartir de lo que ingreso el usuario
    
    res=get_response(ints,intents,text)# intents es el json de referencia
    return res
    

    
######################## SOLO PARA PROBARLO EN CONSOLA ##########################

def start_bot():
    
    texto_us="" # lo que ingresa el usuario
    print(" bienvenido, para salir  escriba salir :")

    while texto_us!="salir":
        texto_us=input()
        res=chatbot_response(texto_us)
        print(res)
    
####################### CHAT-BOT #############################

def bot(texto_us):
        #start_chatbot()
        res=chatbot_response(texto_us)
        return res

'''def start_chatbot():
    #start_intents()
    #start_model()
    start_bot()'''
    
    
# _________________________________MAIN________________________
#from intents_reference import start_intents
#from model_builder import start_model


# Driver program
if __name__ == '__main__':

    #para ejecutar en consola:
    #start_bot()

    #para integrar con whatsapp
    answer=bot(texto_us)
