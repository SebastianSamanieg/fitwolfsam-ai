from langgraph.graph import StateGraph
from typing import TypedDict, List
from agents import (
    nutricionista_agent,
    entrenador_agent,
    motivador_agent,
    router_agent,
)


class AgentState(TypedDict):
    user_input: str
    memory: str
    active_modules: List[str]
    nutricion: str
    entrenamiento: str
    motivacion: str
    final_response: str


def router_node(state):
    active = router_agent(state["user_input"])
    return {"active_modules": active}


def nutricion_node(state):
    if "nutricion" not in state.get("active_modules", []):
        return {"nutricion": ""}
    result = nutricionista_agent(state["user_input"], state["memory"])
    return {"nutricion": result}


def entrenamiento_node(state):
    if "entrenamiento" not in state.get("active_modules", []):
        return {"entrenamiento": ""}
    result = entrenador_agent(state["user_input"], state["memory"])
    return {"entrenamiento": result}


def motivacion_node(state):
    if "motivacion" not in state.get("active_modules", []):
        return {"motivacion": ""}
    result = motivador_agent(state["user_input"], state["memory"])
    return {"motivacion": result}


def respuesta_final_node(state):
    sections = []

    if state.get("nutricion"):
        sections.append(("🥗 Nutrición", state["nutricion"]))
    if state.get("entrenamiento"):
        sections.append(("🏋️ Entrenamiento", state["entrenamiento"]))
    if state.get("motivacion"):
        sections.append(("🔥 Motivación", state["motivacion"]))

    final = "\n\n".join(
        f"**{title}**\n{content}" for title, content in sections
    )

    return {"final_response": final}


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("router", router_node)
    graph.add_node("nutricion", nutricion_node)
    graph.add_node("entrenamiento", entrenamiento_node)
    graph.add_node("motivacion", motivacion_node)
    graph.add_node("respuesta_final", respuesta_final_node)

    graph.set_entry_point("router")
    graph.add_edge("router", "nutricion")
    graph.add_edge("nutricion", "entrenamiento")
    graph.add_edge("entrenamiento", "motivacion")
    graph.add_edge("motivacion", "respuesta_final")
    graph.set_finish_point("respuesta_final")

    return graph.compile()