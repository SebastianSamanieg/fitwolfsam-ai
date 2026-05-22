import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv
from streamlit_mic_recorder import mic_recorder # Importar el componente

# --- INSTRUCCIÓN DE SISTEMA ---
SYSTEM_PROMPT = """
Actúa como un asistente de código AI experto. Tu principal objetivo es dar respuestas **extremadamente prácticas, claras y concisas**.
- **Prioriza la brevedad:** Ve directo al punto. Evita introducciones largas o resúmenes innecesarios.
- **Enfócate en la acción:** Proporciona fragmentos de código directamente aplicables o pasos claros.
- **Lenguaje sencillo:** Explica conceptos complejos de forma simple.
- **Sé útil y directo:** Resuelve la consulta de la manera más eficiente posible.
"""

# --- Configuración Inicial ---
st.set_page_config(page_title="Asistente Voz/Texto (Groq)", page_icon="️🎙️")
st.title("️🎙️ Asistente de Código Voz/Texto (Llama/Groq)")
st.caption("Habla o escribe tu consulta. Respuestas concisas con Llama 3 y Groq.")

# --- Carga de Clave API ---
load_dotenv()
try:
    api_key = st.secrets["GROQ_API_KEY"]
except (FileNotFoundError, KeyError):
    api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("Clave API de Groq no encontrada. Configúrala en los secretos de Streamlit o en un archivo .env como GROQ_API_KEY.")
    st.stop()

# --- Inicialización del Cliente Groq ---
try:
    client = Groq(api_key=api_key)
    LLM_MODEL_NAME = "openai/gpt-oss-20b"
    # Usaremos un modelo Whisper disponible en Groq para STT
    STT_MODEL_NAME = "whisper-large-v3"
except Exception as e:
    st.error(f"Error al inicializar el cliente Groq: {e}")
    st.stop()

# --- Gestión del Historial de Chat (Memoria) ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append(
        {"role": "assistant", "content": f"Hola! Usa el micrófono 🎤 o escribe abajo. (Usando {LLM_MODEL_NAME} y {STT_MODEL_NAME})"}
    )

# --- Mostrar Mensajes Anteriores ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Función para procesar la entrada (texto o audio transcrito) y obtener respuesta ---
def process_input_and_respond(user_prompt: str):
    """Añade el prompt del usuario, llama al LLM y añade la respuesta del asistente."""
    if not user_prompt: # No procesar si el prompt está vacío
         return

    # 1. Añadir y mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # 2. Preparar mensajes para la API LLM (incluir System Prompt)
    messages_for_api = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages_for_api.extend(st.session_state.messages)

    # 3. Llamar a la API LLM de Groq
    try:
        with st.spinner("Pensando... ⚡"):
            chat_completion = client.chat.completions.create(
                messages=messages_for_api,
                model=LLM_MODEL_NAME,
                temperature=0.5,
            )
            assistant_response = chat_completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error al contactar la API LLM de Groq: {e}")
        assistant_response = "Error al generar respuesta del LLM."

    # 4. Añadir y mostrar respuesta del asistente
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    with st.chat_message("assistant"):
        st.markdown(assistant_response)

# --- Entrada de Audio ---
st.write("--- O usa el micrófono ---")
# Usamos 'key' para evitar que se reinicie en cada interacción
# 'callback' podría usarse para procesar inmediatamente, pero lo haremos después
# 'use_container_width=True' para que ocupe el ancho disponible
audio_info = mic_recorder(
    start_prompt="▶️ Grabar",
    stop_prompt="⏹️ Detener",
    key='recorder',
    use_container_width=True
)

# Procesar el audio grabado cuando esté disponible
if audio_info and audio_info['bytes']:
    st.write("Procesando audio...")
    audio_bytes = audio_info['bytes']
    # Opcional: Mostrar reproductor del audio grabado
    # st.audio(audio_bytes)

    # Enviar audio a la API de transcripción de Groq
    try:
        with st.spinner(f"Transcribiendo con {STT_MODEL_NAME}... 🎤"):
            # Groq espera los bytes como un 'file' tuple: (filename, bytes)
            transcription = client.audio.transcriptions.create(
                model=STT_MODEL_NAME,
                file=("audio.wav", audio_bytes) # Damos un nombre de archivo dummy
                # response_format="json" # o "text", "verbose_json", etc.
                # language="es" # Opcional: especificar idioma
            )
            user_prompt_from_audio = transcription.text
            st.write(f"Texto transcrito: *{user_prompt_from_audio}*")

            # Ahora procesa el texto transcrito como entrada del usuario
            process_input_and_respond(user_prompt_from_audio)

    except Exception as e:
        st.error(f"Error durante la transcripción de audio: {e}")
        st.warning("No se pudo procesar el audio. Inténtalo de nuevo o escribe tu consulta.")

# --- Entrada de Texto (Alternativa) ---
st.write("--- O escribe tu consulta ---")
text_prompt = st.chat_input("Escribe tu consulta de código aquí...")

if text_prompt:
    process_input_and_respond(text_prompt)


# --- Opcional: Botón para limpiar historial ---
if len(st.session_state.messages) > 1:
     st.divider() # Separador visual
     if st.button("Limpiar Conversación"):
        initial_message = {"role": "assistant", "content": f"Hola! Usa el micrófono 🎤 o escribe abajo. (Usando {LLM_MODEL_NAME} y {STT_MODEL_NAME})"}
        st.session_state.messages = [initial_message]
        st.rerun() # Recarga la app para reflejar el cambio