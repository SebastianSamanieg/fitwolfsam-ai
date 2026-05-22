import os
from dotenv import load_dotenv
from groq import Groq

# Cargar claves del archivo .env
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Inicialización del agente
class DeporteAgente:
    def __init__(self):
        self.conversacion = []
        self.groq = Groq(api_key=GROQ_API_KEY)

    def procesar_pregunta(self, pregunta):
        # Guardar la pregunta en la conversación
        self.conversacion.append({"pregunta": pregunta})

        # Configuración del mensaje del sistema
        system_message = {
            "content": "Actúa como un experto en deportes. Tu objetivo es proporcionar información precisa y útil sobre competencias, resultados y disciplinas deportivas.",
            "role": "system"
        }

        # Configuración del mensaje del usuario
        user_message = {
            "content": pregunta,
            "role": "user"
        }

        # Enviar la solicitud a Groq
        response = self.groq.chat.completions.create(
            messages=[
                system_message,
                user_message
            ],
            model="openai/gpt-oss-20b"
        )

        # Procesar la respuesta
        respuesta = response.choices[0].message.content

        # Guardar la respuesta en la conversación
        self.conversacion.append({"respuesta": respuesta})

        return respuesta

    def obtener_resultados_recientes(self, deporte):
        # URL para buscar resultados recientes
        url = f"https://www.{deporte.lower()}.com/resultados"

        return url

# Inicialización del agente
agente = DeporteAgente()

def consultar_agente(pregunta):
    respuesta = agente.procesar_pregunta(pregunta)
    return respuesta

if __name__ == "__main__":
    print("Bienvenido al Agente Deportivo IA (Groq)")
    while True:
        user_pregunta = input("¿Cuál es tu pregunta deportiva?: ")
        if user_pregunta.lower() == "salir":
            print("Adiós!")
            break
        respuesta = consultar_agente(user_pregunta)
        print("\nAgente Deportivo:")
        print(respuesta)

        # Preguntar si quiere obtener resultados recientes
        obtener_resultados = input("¿Desea obtener resultados recientes de algún deporte? (si/no): ")
        if obtener_resultados.lower() == "si":
            deporte = input("Ingrese el nombre del deporte: ")
            url = agente.obtener_resultados_recientes(deporte)
            print(f"Resultados recientes de {deporte}: {url}")