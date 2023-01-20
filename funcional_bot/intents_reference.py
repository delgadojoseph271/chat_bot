import json
def guardar_json(datos):
  archivo = open('/intents.json', 'w+')
  json.dump(datos,archivo,indent=4)

#intents: grupos de conversaciones tipicas para nuestro objetivo
# patterns: posibles interacciones con el usuario

#dic={"intents:[[{"key":["vlores"]}],"dic2"]}

def start_intents():
    biblioteca={"intents":
                [
                    {"tag":"saludos",
                    "patterns":["hola",
                                "buenos dias",
                                "buenas tardes",
                                "buenas noches",
                                "como estas",
                                "hay alguien ahi?",
                                "hey",
                                "saludos",
                                "que tal"                      
                                ],
                    "responses":["Hola soy AUTO-BOT , tu asesor de compras para tu futuro automóvil.\n ¿En qué puedo ayudarte? "
                                ],
                    "context":[""]
                    },
                
                    {"tag":"compras",
                    "patterns":["consultar precios",
                                "comprar un auto",
                                "averiguar precio",
                                "busco un coche",
                                "informacion",
                                "necesito ayuda con",
                                "me puede colaborar",
                                "busco un auto",
                                "que carros tienen"                      
                                ],
                    "responses":["Perfecto, ¿Quieres probar una busqueda directa o deseas una recomendacion basada en características?" 
                                ],
                    "context":[""]
                    },

                    {"tag":"busqueda_directa",
                        "patterns":["busqueda directa",
                                    "directo",
                                    "de inmediato",
                                    "busqueda inmediata",
                                ],
                        "responses":[ "¿Qué tipo de vehículo te gustaría. Por ejemplo: sedán, pickup, camioneta..."
                                    ],
                        "context":[""]
                        },
                
                    {"tag":"tipo",
                    "patterns":["sedan",
                                "pickup",
                                "camioneta",
                                "coupe",
                                "deportivos"                 
                                ],
                    "responses":["¿Alguna marca en particular?",
                                "¿Tiene alguna marca en mente?",
                                "¿Qué marca le gustaría?"
                                ],
                    "context":[""]
                    },
                
                    {"tag":"marca",
                    "patterns":["nissan",
                                "honda",
                                "toyota",
                                "ford",
                                "isuzu",
                                "audi",
                                "bmw",
                                "subaru",
                                "mitsubihi",
                                "corvette"              
                                ],
                    "responses":["Listo, procederé a realizar la busqueda en bodéga del tipo y marca seleccionado",
                                ],
                    "context":[""]
                    },
                                
                    {"tag":"recomendacion",
                        "patterns":["recomendación",
                                    "recomiendes algo",
                                    "necesito recomendación",
                                    "que me recomiendas",
                                    "necesito algunas específicaciones"
                                    ],
                    "responses":["Buena elección. por favor siga estas instrucciones: \n Revisaremos las característica una a una. Por ejemplo, año del auto: 2020 . Si necesitas ayuda con algún concepto, escribe la palabra asistencia."
                                    ],
                        "context":[""]
                        },

                    {"tag":"anho_del_auto",
                        "patterns":["año",
                                    "año:",
                                    "del año"
                                ],
                        "responses":[ "¿Con cuantos caballos de fuerza?"
                                    ],
                        "context":[""]
                        },
                
                    {"tag":"caballos_de_fuerza",
                        "patterns":["120 caballos de fuerza",
                                    "caballos de fuerza:",
                                    "potencia de:"
                                ],
                        "responses":[ "¿Qué precio tiene en mente?"
                                    ],
                        "context":[""]
                        },  
                    {"tag":"precio_esperado",
                        "patterns":["12 000 dólares",
                                    "precio: 30000",
                                    "costo: 25000"
                                ],
                        "responses":[ "¿Cuál quiere que sea el rendimiento de combustible?"
                                    ],
                        "context":[""]
                        },
                
                    {"tag":"consumo_combustible",
                        "patterns":["cosumo:",
                                    "que sea económico",
                                    "50 kilómetros por galón"
                                ],
                        "responses":[ "¿Cuál quiere que sea el tipo de combustible? \n Gasolina, Diesel o Eléctrico."
                                    ],
                        "context":[""]
                        },
                    {"tag":"tipo_de_combustible",
                        "patterns":["combustible:",
                                    "gasolina",
                                    "diesel",
                                    "eléctrico"
                                ],
                        "responses":[ "¿Cuántas plazas (asientos) aproximadamente necesita?"
                                    ],
                        "context":[""]
                        },
                    {"tag":"número_de_asientos",
                        "patterns":["asientos:",
                                    "plazas:",
                                    "espacioso",
                                    "2 asientos"
                                ],
                        "responses":[ "¿Transmisión manual o automática?."
                                    ],
                        "context":[""]
                        },
                    {"tag":"tipo_de_transmisión",
                        "patterns":["transmisión manual",
                                    "transmisión automática",
                                    "manual",
                                    "automática"
                                ],
                        "responses":[ "Listo. Ahora realizaré una estimación del vehículo disponible que mejor se ajusta a tus necesidades.\n Escribe 'recomendar ahora' para continuar."
                                    ],
                        "context":[""]
                        },

                    {"tag":"recomendar_ahora",
                    "patterns":["recomendar ahora"
                                ],
                    "responses":["Revisando características en bodega"
                                ],
                    "context":[""]
                    },
                    

                    {"tag":"asistencia",
                    "patterns":["asistencia"
                                ],
                    "responses":["¿Para cuál concepto necesita ayuda?\n Año del auto. Potencia en caballos de fuerza. Precio esperado. Consumo de combustible. Tipo de combustible. Número de asientos. Tipo de transmisión"
                                ],
                    "context":[""]
                    },
                    
                    {"tag":"despedidas",
                    "patterns":["chao",
                                "adios",
                                "hasta luego",
                                "nos vemos",
                                "bye",
                                "hasta pronto",
                                "hasta la proxima"
                                ],
                    "responses":["hasta luego, tenga un buen dia"
                                ],
                    "context":[""]
                    },
                
                    {"tag":"agradecimientos",
                    "patterns":["gracias",
                                "muchas gracias",
                                "mil gracias",
                                "muy amable",
                                "se lo agradezco",
                                "fue de ayuda",
                                "gracias por la ayuda",
                                "muy agradecido",
                                "gracias por su tiempo",
                                "ty"
                                ],
                    "responses":["de nada",
                                "feliz por ayudarlo",
                                "gracias a usted",
                                "estamos para servirle",
                                "fue un placer"
                                ],
                    "context":[""]
                    },
                    {"tag":"norespuesta",
                    "patterns":[""],
                    "responses":["no se detecto una respuesta",
                                ],
                    "context":[""]                    
                    }
                ] 
            }
    guardar_json(biblioteca)

# _________________________________MAIN________________________

# Driver program
if __name__ == '__main__':       
    start_intents()