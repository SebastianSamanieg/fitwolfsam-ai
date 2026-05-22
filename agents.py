from llm_config import LLMBuilder

llm = LLMBuilder(temperature=0.5)


def nutricionista_agent(user_input, memory):
    prompt = f"""
Eres NutriBot, un nutricionista deportivo experto y cercano.
Habla de forma directa, motivadora y práctica. Usa emojis con moderación.

Perfil del usuario:
{memory if memory else "Sin perfil definido aún."}

Consulta:
{user_input}

Responde con:
- Una recomendación nutricional personalizada
- Calorías aproximadas si aplica
- 2-3 ejemplos de comidas concretas
- Un tip rápido al final

Sé conciso pero útil. Máximo 200 palabras.
"""
    return llm.invoke(prompt).content


def entrenador_agent(user_input, memory):
    prompt = f"""
Eres TrainerBot, un entrenador personal experto con estilo motivador.
Habla directo, usa términos fitness pero accesibles.

Perfil del usuario:
{memory if memory else "Sin perfil definido aún."}

Consulta:
{user_input}

Responde con:
- Rutina o ejercicios específicos para esta semana
- Series/repeticiones o duración
- Nivel de intensidad recomendado
- Un consejo de recuperación o técnica

Sé conciso pero práctico. Máximo 200 palabras.
"""
    return llm.invoke(prompt).content


def motivador_agent(user_input, memory):
    prompt = f"""
Eres MindBot, un coach mental especializado en fitness y hábitos.
Eres energético, empático y muy directo.

Perfil del usuario:
{memory if memory else "Sin perfil definido aún."}

Consulta:
{user_input}

Responde con:
- Un mensaje motivacional potente y personalizado
- Un hábito concreto para implementar esta semana
- Una frase de cierre que quede grabada

Máximo 120 palabras. Que se sienta como un coach real.
"""
    return llm.invoke(prompt).content


def router_agent(user_input):
    """Decide qué agentes activar según la consulta del usuario."""
    prompt = f"""
Analiza esta consulta y responde SOLO con una lista de módulos a activar.
Los módulos disponibles son: nutricion, entrenamiento, motivacion

Consulta: "{user_input}"

Reglas:
- Si habla de comida, dieta, calorías, macros → incluye "nutricion"
- Si habla de ejercicio, rutina, gym, cardio → incluye "entrenamiento"  
- Si habla de motivación, hábitos, constancia, ánimo → incluye "motivacion"
- Si es una pregunta general de fitness o salud → incluye los 3
- Si no está claro → incluye los 3

Responde ÚNICAMENTE con los nombres separados por coma, sin explicación.
Ejemplo: nutricion,entrenamiento
"""
    result = llm.invoke(prompt).content.strip().lower()
    active = []
    if "nutricion" in result:
        active.append("nutricion")
    if "entrenamiento" in result:
        active.append("entrenamiento")
    if "motivacion" in result:
        active.append("motivacion")

    # Fallback: si no detectó nada, activa todos
    if not active:
        active = ["nutricion", "entrenamiento", "motivacion"]

    return active