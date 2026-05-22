import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS
import pygame
import io
import threading
import re

# --- Configuración Inicial de la Página ---
st.set_page_config(page_title="Asistente Voz/Texto (Groq+gTTS)", page_icon="️🎙️")

# --- Carga de Clave API ---
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("Clave API de Groq no encontrada...")
    st.stop()
# else: # Ya no es tan necesario mostrar este info en cada rerun
    # st.info("Clave API de Groq cargada desde .env.")

# --- INSTRUCCIÓN DE SISTEMA ---
SYSTEM_PROMPT = "..." # Mantenido igual

# --- Título y Caption ---
st.title("️🎙️ Asistente de Código Voz/Texto (Llama/Groq + gTTS)")
st.caption("Habla o escribe tu consulta. Respuestas concisas con Llama 3, Groq y audio gTTS.")

# --- Inicialización del Cliente Groq ---
try:
    client = Groq(api_key=api_key)
    LLM_MODEL_NAME = "openai/gpt-oss-20b"
    STT_MODEL_NAME = "whisper-large-v3"
except Exception as e:
    st.error(f"Error al inicializar el cliente Groq: {e}")
    st.stop()

# --- Inicialización de Pygame Mixer ---
if "pygame_mixer_initialized" not in st.session_state:
    try:
        pygame.mixer.init()
        st.session_state.pygame_mixer_initialized = True
    except Exception as e:
        st.session_state.pygame_mixer_initialized = False

# --- Función para limpiar Markdown ---
def clean_markdown(md_text):
    # ... (mantenida igual) ...
    text = re.sub(r'```.*?```', '', md_text, flags=re.DOTALL)
    text = re.sub(r'`[^`]*`', '', text)
    text = re.sub(r'^\#{1,6}\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'(\*\*|__)(.*?)\1', r'\2', text)
    text = re.sub(r'(\*|_)(.*?)\1', r'\2', text)
    text = re.sub(r'~~(.*?)~~', r'\1', text)
    text = re.sub(r'!\[(.*?)\]\(.*?\)', r'\1', text)
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
    text = re.sub(r'^\s*[\*\-\+]\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\n{2,}', '\n', text)
    return text.strip()

# --- Función TTS con gTTS ---
gtts_lock = threading.Lock()
def generate_audio_bytes(text_to_speak: str, lang: str = 'es') -> io.BytesIO | None:
    # ... (mantenida igual) ...
    if not text_to_speak:
        return None
    cleaned_text = clean_markdown(text_to_speak)
    if not cleaned_text:
        return None
    with gtts_lock:
        try:
            tts = gTTS(text=cleaned_text, lang=lang, slow=False)
            audio_fp = io.BytesIO()
            tts.write_to_fp(audio_fp)
            audio_fp.seek(0)
            return audio_fp
        except ConnectionError:
            st.error("Error de conexión con gTTS.")
            return None
        except Exception as e:
            st.error(f"Error en gTTS: {e}")
            return None

# --- Gestión del Historial de Chat y Estado de Entrada ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": f"Hola! (Usando **{LLM_MODEL_NAME}**)"}]
if "last_assistant_response" not in st.session_state:
    st.session_state.last_assistant_response = None
if "last_audio_bytes" not in st.session_state:
    st.session_state.last_audio_bytes = None
if "user_input_processed" not in st.session_state: # Bandera para controlar el procesamiento
    st.session_state.user_input_processed = True # Inicia como True (no hay nada que procesar)
if "current_user_input" not in st.session_state: # Para almacenar la entrada pendiente
    st.session_state.current_user_input = None

# --- Mostrar Mensajes Anteriores ---
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and i == len(st.session_state.messages) - 1 and st.session_state.last_audio_bytes:
            st.audio(st.session_state.last_audio_bytes, format="audio/mp3")

# --- Función para procesar la entrada (texto o audio transcrito) y obtener respuesta ---
def process_input_and_respond(user_prompt: str): # Eliminado play_response_audio_automatically
    if not user_prompt:
         return

    st.session_state.messages.append({"role": "user", "content": user_prompt})

    messages_for_api = [{"role": "system", "content": SYSTEM_PROMPT}]
    history_for_api = [{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.messages if msg["role"] in ["user", "assistant"]]
    messages_for_api.extend(history_for_api)

    assistant_response = "Error al generar respuesta del LLM." # Default
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
        # assistant_response ya tiene el mensaje de error

    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    st.session_state.last_assistant_response = assistant_response
    st.session_state.last_audio_bytes = None # Resetear audio anterior

    if assistant_response:
        audio_bytes_gen = generate_audio_bytes(assistant_response)
        if audio_bytes_gen:
            st.session_state.last_audio_bytes = audio_bytes_gen

    st.session_state.user_input_processed = True # Marcar como procesado
    st.session_state.current_user_input = None   # Limpiar la entrada pendiente
    # st.rerun() # Eliminamos el rerun explícito aquí, Streamlit rerunea naturalmente con widgets


# --- Lógica de Procesamiento de Entradas ---
# Esto se ejecutará en cada rerun, pero solo procesará si hay nueva entrada pendiente.

# 1. Capturar nueva entrada de texto
text_prompt_input = st.chat_input("Escribe tu consulta de código aquí...", key="chat_input_widget")
if text_prompt_input and st.session_state.current_user_input != text_prompt_input : # Si hay nueva entrada de texto
    st.session_state.current_user_input = text_prompt_input
    st.session_state.user_input_processed = False # Marcar que hay algo que procesar
    # No llamamos a process_input_and_respond aquí directamente, se hará abajo

# 2. Capturar nueva entrada de audio
audio_info = mic_recorder(
    start_prompt="▶️ Grabar",
    stop_prompt="⏹️ Detener",
    key='recorder', # La key es importante para que el estado se mantenga
    use_container_width=True
)

# Si hay nuevos bytes de audio Y NO estamos ya procesando una entrada de texto
if audio_info and audio_info.get('bytes') and st.session_state.user_input_processed:
    # Verificamos si es un "nuevo" evento de audio para evitar reprocesar el mismo audio si el usuario no interactúa
    # Esto es un poco más complejo con mic_recorder porque no tiene un "on_submit" claro como chat_input
    # Una forma es comparar con el ID del audio o el timestamp si estuviera disponible, o usar un flag.
    # Por simplicidad, asumiremos que si 'bytes' está presente y no hay otra entrada, es nuevo.
    # Para hacerlo más robusto, mic_recorder podría necesitar un callback que setee un flag.

    # Para este ejemplo, procesaremos si hay audio y user_input_processed es True
    # (lo que significa que no hay una entrada de texto pendiente)
    audio_bytes_input = audio_info['bytes']
    st.write("Procesando audio...")
    try:
        with st.spinner(f"Transcribiendo con {STT_MODEL_NAME}... 🎤"):
            transcription = client.audio.transcriptions.create(
                model=STT_MODEL_NAME,
                file=("audio.wav", audio_bytes_input)
            )
            user_prompt_from_audio = transcription.text
            st.write(f"Texto transcrito: *{user_prompt_from_audio}*")
            st.session_state.current_user_input = user_prompt_from_audio # Guardar para procesar
            st.session_state.user_input_processed = False # Marcar que hay algo que procesar
            # mic_recorder resetea su estado interno después de devolver los bytes,
            # por lo que no debería dispararse continuamente sin nueva grabación.

    except Exception as e:
        st.error(f"Error durante la transcripción de audio: {e}")
        st.warning("No se pudo procesar el audio. Inténtalo de nuevo o escribe tu consulta.")
        st.session_state.user_input_processed = True # Resetear si falla la transcripción

# 3. Procesar la entrada pendiente (si existe y no ha sido procesada)
if not st.session_state.user_input_processed and st.session_state.current_user_input:
    process_input_and_respond(st.session_state.current_user_input)
    # No se necesita st.rerun() aquí, porque process_input_and_respond actualiza session_state,
    # y Streamlit rerunea automáticamente cuando el estado de los widgets (como chat_input) cambia
    # o cuando session_state es modificado. El problema anterior era el st.rerun() *dentro*
    # de process_input_and_respond que creaba el bucle si la entrada no se consumía.


# --- Opcional: Botón para limpiar historial ---
if len(st.session_state.messages) > 1:
     st.divider()
     if st.button("Limpiar Conversación"):
        st.session_state.messages = [{"role": "assistant", "content": f"Hola! (Usando **{LLM_MODEL_NAME}**)"}]
        st.session_state.last_assistant_response = None
        st.session_state.last_audio_bytes = None
        st.session_state.user_input_processed = True # No hay nada pendiente
        st.session_state.current_user_input = None
        if st.session_state.get("pygame_mixer_initialized", False):
            pygame.mixer.music.stop()
        st.rerun() # Aquí sí es útil para refrescar la UI inmediatamente después de limpiar