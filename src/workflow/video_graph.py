from typing import TypedDict

from langgraph.graph import StateGraph
from langgraph.graph import END


from src.agents.script_agent import generate_script


class VideoState(TypedDict):
    topic: str
    duration: str
    language: str
    style: str
    script: str


def script_node(state):

    script = generate_script(
        topic=state["topic"],
        duration=state["duration"],
        language=state["language"],
        style=state["style"]
    )

    state["script"] = script

    return state


def build_graph():

    graph = StateGraph(VideoState)

    graph.add_node(
        "script_generation",
        script_node
    )

    graph.set_entry_point(
        "script_generation"
    )

    graph.add_edge(
        "script_generation",
        END
    )

    return graph.compile()