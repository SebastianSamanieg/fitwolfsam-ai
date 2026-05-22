import time
from llm_config import LLMBuilder

llm_nutricion     = LLMBuilder(temperature=0.85, model_override="llama-3.3-70b-versatile")
llm_entrenamiento = LLMBuilder(temperature=0.85, model_override="llama-3.3-70b-versatile")
llm_motivacion    = LLMBuilder(temperature=0.85, model_override="llama-3.3-70b-versatile")
llm_router        = LLMBuilder(temperature=0.0,  model_override="llama-3.1-8b-instant")


def nutricionista_agent(user_input, memory):
    prompt = f"""Eres NutriBot, nutricionista deportivo experto. Responde en español.

PERFIL: {memory if memory else "Sin perfil."}
CONSULTA: {user_input}

## 📊 Macros diarios
Calorías: X kcal | Proteínas: Xg | Carbos: Xg | Grasas: Xg

## 🍽️ Plan de comidas
**Desayuno ~X kcal:** [alimento + gramos]
**Media mañana ~X kcal:** [alimento + gramos]
**Almuerzo ~X kcal:** [alimento + gramos]
**Merienda ~X kcal:** [alimento + gramos]
**Cena ~X kcal:** [alimento + gramos]

## 🎯 Estrategia y tips
[3 tips clave con justificación]"""
    return llm_nutricion.invoke(prompt).content


def entrenador_agent(user_input, memory):
    nivel = "principiante/sedentario" if memory and "sedentario" in memory.lower() else "intermedio"
    prompt = f"""Eres TrainerBot, entrenador personal experto. Responde en español.

PERFIL: {memory if memory else "Sin perfil."}
NIVEL ESTIMADO: {nivel}
CONSULTA: {user_input}

Genera la rutina COMPLETA día por día. USA ESTE FORMATO EXACTO para cada día:

---
**LUNES — Pecho y Tríceps**
Calentamiento (10 min): [3 ejercicios específicos con duración]
| Ejercicio | Series | Reps | Descanso |
|-----------|--------|------|----------|
| Press de banca | 4 | 10-12 | 60s |
| [siguiente] | X | X | Xs |
| [siguiente] | X | X | Xs |
| [siguiente] | X | X | Xs |
Accesorio: [ejercicio aislado x series x reps]
Enfriamiento: [estiramiento específico 5 min]

**MARTES — Espalda y Bíceps**
[mismo formato]

**MIÉRCOLES — Descanso activo**
[20-30 min cardio ligero o movilidad]

**JUEVES — Piernas**
[mismo formato con tabla]

**VIERNES — Hombros y Core**
[mismo formato con tabla]
---

Al final agrega solo:
## 📈 Progresión
[cómo aumentar peso/reps semana a semana en 2-3 líneas]"""
    return llm_entrenamiento.invoke(prompt).content


def motivador_agent(user_input, memory):
    prompt = f"""Eres MindBot, coach mental experto. Responde en español.

PERFIL: {memory if memory else "Sin perfil."}
CONSULTA: {user_input}

## 🧠 Por qué el cerebro sabotea tus hábitos
[neurociencia simple en 3-4 líneas]

## ⚡ 4 Estrategias que funcionan
**1. Habit stacking:** [ejemplo concreto con horario]
**2. Intención de implementación:** "Cuando [X], haré [Y] en [Z]"
**3. Recompensa inmediata:** [qué hacer justo al terminar]
**4. Plan de fallo:** [qué hacer exactamente el día que no quieras]

## 📅 Tu semana en acción
Lun: [acción muy concreta]
Mar: [acción muy concreta]
Mié: [acción muy concreta]
Jue: [acción muy concreta]
Vie: [acción muy concreta]
Sáb: [acción muy concreta]
Dom: [revisión/ajuste]

## 💬 Para llevar
[Una frase poderosa y personalizada, no un cliché]"""
    return llm_motivacion.invoke(prompt).content


def router_agent(user_input):
    prompt = f'Texto: "{user_input}"\nResponde solo con palabras separadas por coma de esta lista: nutricion, entrenamiento, motivacion'
    result = llm_router.invoke(prompt).content.strip().lower()
    active = []
    if "nutricion" in result:
        active.append("nutricion")
    if "entrenamiento" in result:
        active.append("entrenamiento")
    if "motivacion" in result:
        active.append("motivacion")
    return active if active else ["nutricion", "entrenamiento", "motivacion"]