import streamlit as st
import os
import math
from dotenv import load_dotenv
from graph import build_graph

load_dotenv()

# ── Página ──────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FitWolfSam AI",
    page_icon="🐺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f !important;
    color: #e8e6e0 !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stSidebar"] {
    background: #0f0f18 !important;
    border-right: 1px solid #1e1e2e !important;
}

/* ── Header principal ── */
.fw-header {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 28px 0 18px;
    border-bottom: 1px solid #1e1e2e;
    margin-bottom: 28px;
}
.fw-logo {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.6rem;
    letter-spacing: 3px;
    background: linear-gradient(135deg, #ff6b35 0%, #f7c59f 60%, #ffffff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
}
.fw-tagline {
    font-size: 0.78rem;
    color: #666680;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 4px;
}
.fw-pulse {
    width: 10px; height: 10px;
    border-radius: 50%;
    background: #ff6b35;
    box-shadow: 0 0 0 0 rgba(255,107,53,0.4);
    animation: pulse-ring 2s infinite;
    flex-shrink: 0;
}
@keyframes pulse-ring {
    0%   { box-shadow: 0 0 0 0 rgba(255,107,53,0.5); }
    70%  { box-shadow: 0 0 0 10px rgba(255,107,53,0); }
    100% { box-shadow: 0 0 0 0 rgba(255,107,53,0); }
}

/* ── Sidebar widgets ── */
[data-testid="stSidebar"] label {
    color: #a0a0b8 !important;
    font-size: 0.78rem !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
}
[data-testid="stSidebar"] .stNumberInput input,
[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {
    background: #16161f !important;
    border: 1px solid #2a2a3e !important;
    color: #e8e6e0 !important;
    border-radius: 8px !important;
}

/* ── IMC card ── */
.imc-card {
    background: linear-gradient(135deg, #1a1a28 0%, #12121c 100%);
    border: 1px solid #2a2a3e;
    border-radius: 14px;
    padding: 18px 20px;
    margin: 16px 0;
    text-align: center;
}
.imc-value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.8rem;
    letter-spacing: 2px;
    line-height: 1;
}
.imc-label {
    font-size: 0.72rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #666680;
    margin-top: 4px;
}
.imc-cat {
    font-size: 0.85rem;
    font-weight: 600;
    margin-top: 8px;
    padding: 4px 12px;
    border-radius: 20px;
    display: inline-block;
}

/* ── Botón guardar perfil ── */
[data-testid="stSidebar"] .stButton button {
    background: linear-gradient(135deg, #ff6b35, #e8542a) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    font-size: 0.8rem !important;
    padding: 10px 20px !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: opacity 0.2s !important;
}
[data-testid="stSidebar"] .stButton button:hover {
    opacity: 0.85 !important;
}

/* ── Área de chat ── */
.stChatMessage {
    background: transparent !important;
}
[data-testid="stChatMessageContent"] {
    background: #13131e !important;
    border: 1px solid #1e1e2e !important;
    border-radius: 14px !important;
    color: #e8e6e0 !important;
}

/* ── Burbuja usuario ── */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"] {
    background: linear-gradient(135deg, #1f1a2e, #16141f) !important;
    border-color: #ff6b3530 !important;
}

/* ── Cards de respuesta ── */
.response-card {
    background: linear-gradient(145deg, #13131e 0%, #0f0f18 100%);
    border: 1px solid #2a2a3e;
    border-radius: 16px;
    padding: 22px 24px;
    margin: 10px 0;
    position: relative;
    overflow: hidden;
}
.response-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    border-radius: 16px 0 0 16px;
}
.card-nutricion::before  { background: linear-gradient(180deg, #4ade80, #22c55e); }
.card-entrenamiento::before { background: linear-gradient(180deg, #60a5fa, #3b82f6); }
.card-motivacion::before  { background: linear-gradient(180deg, #f97316, #ff6b35); }

.card-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.15rem;
    letter-spacing: 2px;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.card-nutricion .card-title    { color: #4ade80; }
.card-entrenamiento .card-title { color: #60a5fa; }
.card-motivacion .card-title   { color: #f97316; }

.card-body {
    font-size: 0.9rem;
    line-height: 1.7;
    color: #c8c6c0;
}

/* ── Input de chat ── */
[data-testid="stChatInput"] {
    background: #13131e !important;
    border: 1px solid #2a2a3e !important;
    border-radius: 14px !important;
    color: #e8e6e0 !important;
}
[data-testid="stChatInput"] textarea {
    color: #e8e6e0 !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Mic section ── */
.mic-section {
    background: #0f0f18;
    border: 1px dashed #2a2a3e;
    border-radius: 14px;
    padding: 16px 20px;
    margin: 12px 0 20px;
    display: flex;
    align-items: center;
    gap: 12px;
}
.mic-label {
    font-size: 0.75rem;
    color: #555570;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

/* ── Divider ── */
.fw-divider {
    border: none;
    border-top: 1px solid #1e1e2e;
    margin: 24px 0;
}

/* ── Spinner override ── */
[data-testid="stSpinner"] {
    color: #ff6b35 !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0a0f; }
::-webkit-scrollbar-thumb { background: #2a2a3e; border-radius: 3px; }

/* ── Welcome message ── */
.welcome-box {
    background: linear-gradient(135deg, #13131e 0%, #0f0f18 100%);
    border: 1px solid #2a2a3e;
    border-radius: 16px;
    padding: 32px 36px;
    text-align: center;
    margin: 20px 0 32px;
}
.welcome-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.5rem;
    letter-spacing: 3px;
    color: #e8e6e0;
    margin-bottom: 8px;
}
.welcome-sub {
    font-size: 0.85rem;
    color: #55556a;
    line-height: 1.6;
}
.pill {
    display: inline-block;
    background: #1e1e2e;
    border: 1px solid #2a2a3e;
    border-radius: 20px;
    padding: 5px 14px;
    font-size: 0.75rem;
    color: #8888a8;
    margin: 4px 3px;
    letter-spacing: 0.5px;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ─────────────────────────────────────────────────────────────────
def calcular_imc(peso, altura_cm):
    h = altura_cm / 100
    return round(peso / (h * h), 1)

def categoria_imc(imc):
    if imc < 18.5:
        return ("Bajo peso", "#60a5fa")
    elif imc < 25:
        return ("Peso normal", "#4ade80")
    elif imc < 30:
        return ("Sobrepeso", "#facc15")
    else:
        return ("Obesidad", "#f97316")

def parse_response_cards(text):
    """Separa la respuesta final en secciones por sección."""
    sections = {"nutricion": "", "entrenamiento": "", "motivacion": ""}
    current = None
    lines = []
    for line in text.split("\n"):
        if "Nutrición" in line or "nutricion" in line.lower():
            if current and lines:
                sections[current] = "\n".join(lines).strip()
            current = "nutricion"; lines = []
        elif "Entrenamiento" in line or "entrenamiento" in line.lower():
            if current and lines:
                sections[current] = "\n".join(lines).strip()
            current = "entrenamiento"; lines = []
        elif "Motivación" in line or "motivacion" in line.lower():
            if current and lines:
                sections[current] = "\n".join(lines).strip()
            current = "motivacion"; lines = []
        else:
            if current:
                lines.append(line)
    if current and lines:
        sections[current] = "\n".join(lines).strip()
    return sections


def render_response_cards(response_text):
    sections = parse_response_cards(response_text)

    card_meta = [
        ("nutricion",     "🥗", "NUTRICIÓN",     "card-nutricion"),
        ("entrenamiento", "🏋️", "ENTRENAMIENTO", "card-entrenamiento"),
        ("motivacion",    "🔥", "MOTIVACIÓN",    "card-motivacion"),
    ]
    for key, emoji, title, css_class in card_meta:
        content = sections.get(key, "").strip()
        if content:
            st.markdown(f"""
            <div class="response-card {css_class}">
                <div class="card-title">{emoji} {title}</div>
                <div class="card-body">{content}</div>
            </div>
            """, unsafe_allow_html=True)


# ── Estado ───────────────────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_profile" not in st.session_state:
    st.session_state.user_profile = ""
if "graph" not in st.session_state:
    st.session_state.graph = build_graph()
if "audio_processed_id" not in st.session_state:
    st.session_state.audio_processed_id = None


# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="font-family:'Bebas Neue',sans-serif; font-size:1.5rem;
                letter-spacing:3px; color:#ff6b35; padding: 20px 0 4px;">
        🐺 FITWOLFSAM
    </div>
    <div style="font-size:0.68rem; color:#44445a; letter-spacing:2px;
                text-transform:uppercase; margin-bottom:24px;">
        AI COACH PERSONAL
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="font-size:0.72rem; color:#666680; letter-spacing:2px; text-transform:uppercase; margin-bottom:12px;">TU PERFIL</div>', unsafe_allow_html=True)

    edad   = st.number_input("Edad", 16, 80, 25, key="edad")
    peso   = st.number_input("Peso (kg)", 40, 200, 75, key="peso")
    altura = st.number_input("Altura (cm)", 140, 220, 175, key="altura")
    objetivo = st.selectbox(
        "Objetivo",
        ["Bajar de peso", "Ganar masa muscular", "Mantener y tonificar", "Mejorar resistencia"],
        key="objetivo"
    )
    nivel = st.selectbox(
        "Nivel de actividad",
        ["Sedentario", "Principiante", "Intermedio", "Avanzado"],
        key="nivel"
    )

    # IMC en tiempo real
    imc = calcular_imc(peso, altura)
    cat, color = categoria_imc(imc)
    st.markdown(f"""
    <div class="imc-card">
        <div class="imc-value" style="color:{color};">{imc}</div>
        <div class="imc-label">Índice de Masa Corporal</div>
        <div class="imc-cat" style="background:{color}22; color:{color};">{cat}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("💾  Guardar perfil"):
        st.session_state.user_profile = f"""
Edad: {edad} años
Peso: {peso} kg
Altura: {altura} cm
IMC: {imc} ({cat})
Objetivo: {objetivo}
Nivel: {nivel}
""".strip()
        st.success("✓ Perfil actualizado")

    st.markdown('<hr class="fw-divider">', unsafe_allow_html=True)

    # Limpiar chat
    if st.button("🗑️  Limpiar conversación"):
        st.session_state.chat_history = []
        st.rerun()


# ── Layout principal ─────────────────────────────────────────────────────────
col_main, col_gap = st.columns([1, 0.02])

with col_main:
    # Header
    st.markdown("""
    <div class="fw-header">
        <div class="fw-pulse"></div>
        <div>
            <div class="fw-logo">FitWolfSam AI</div>
            <div class="fw-tagline">Tu coach de nutrición &amp; entrenamiento</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Bienvenida si no hay historial
    if not st.session_state.chat_history:
        st.markdown("""
        <div class="welcome-box">
            <div class="welcome-title">¿En qué te ayudo hoy?</div>
            <div class="welcome-sub">
                Cuéntame tu consulta — nutrición, rutina de ejercicio, motivación<br>
                o todo a la vez. Habla o escribe lo que necesitas.
            </div>
            <br>
            <span class="pill">🥗 Planes alimenticios</span>
            <span class="pill">🏋️ Rutinas semanales</span>
            <span class="pill">🔥 Motivación real</span>
            <span class="pill">🎙️ Entrada por voz</span>
        </div>
        """, unsafe_allow_html=True)

    # Historial de chat
    for role, msg, is_structured in st.session_state.chat_history:
        if role == "user":
            with st.chat_message("user"):
                st.write(msg)
        else:
            with st.chat_message("assistant", avatar="🐺"):
                if is_structured:
                    render_response_cards(msg)
                else:
                    st.write(msg)

    # ── Entrada por voz ──────────────────────────────────────────────────────
    groq_key = os.getenv("GROQ_API_KEY")
    voice_prompt = None

    if groq_key:
        try:
            from streamlit_mic_recorder import mic_recorder

            st.markdown('<div class="mic-label">🎙️ &nbsp;ENTRADA POR VOZ</div>', unsafe_allow_html=True)

            with st.container():
                audio_info = mic_recorder(
                    start_prompt="⏺ Grabar",
                    stop_prompt="⏹ Detener",
                    key="recorder",
                    use_container_width=False,
                )

            if audio_info and audio_info.get("bytes"):
                audio_id = hash(audio_info["bytes"])
                if audio_id != st.session_state.audio_processed_id:
                    st.session_state.audio_processed_id = audio_id
                    from groq import Groq
                    client = Groq(api_key=groq_key)
                    with st.spinner("🎤 Transcribiendo..."):
                        transcription = client.audio.transcriptions.create(
                            model="whisper-large-v3",
                            file=("audio.wav", audio_info["bytes"]),
                        )
                    voice_prompt = transcription.text
                    st.caption(f"🗣️ *\"{voice_prompt}\"*")

        except ImportError:
            st.caption("_Instala `streamlit-mic-recorder` para habilitar la voz._")
    else:
        st.caption("_Agrega `GROQ_API_KEY` en .env para habilitar entrada por voz._")

    # ── Input texto ──────────────────────────────────────────────────────────
    text_prompt = st.chat_input("Escribe tu consulta al coach...")

    # ── Procesar cualquier entrada ───────────────────────────────────────────
    user_input = voice_prompt or text_prompt

    if user_input:
        st.session_state.chat_history.append(("user", user_input, False))

        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant", avatar="🐺"):
            with st.spinner("🐺 Analizando tu consulta..."):
                result = st.session_state.graph.invoke({
                    "user_input": user_input,
                    "memory": st.session_state.user_profile,
                    "active_modules": [],
                    "nutricion": "",
                    "entrenamiento": "",
                    "motivacion": "",
                    "final_response": "",
                })
            respuesta = result["final_response"]
            render_response_cards(respuesta)

        st.session_state.chat_history.append(("assistant", respuesta, True))
        st.rerun()