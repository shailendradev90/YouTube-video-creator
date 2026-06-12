from typing import TypedDict

from langgraph.graph import StateGraph
from langgraph.graph import END

from src.agents.script_agent import generate_script
from src.agents.voice_agent import generate_voice
from src.agents.media_agent import download_media


class VideoState(TypedDict):
    topic: str
    duration: str
    language: str
    style: str
    script: str
    audio_path: str
    media_files: list


def script_node(state):
    script = generate_script(
        topic=state["topic"],
        duration=state["duration"],
        language=state["language"],
        style=state["style"]
    )
    state["script"] = script
    return state


def voice_node(state):
    audio_path = generate_voice(
        state["script"]
    )
    state["audio_path"] = audio_path
    return state


def media_node(state):
    files = download_media(state["topic"])
    state["media_files"] = files
    return state


def build_graph():
    graph = StateGraph(VideoState)

    graph.add_node(
        "script_generation",
        script_node
    )

    graph.add_node(
        "voice_generation",
        voice_node
    )

    graph.add_node(
        "media_generation",
        media_node
    )

    graph.set_entry_point(
        "script_generation"
    )

    graph.add_edge(
        "script_generation",
        "voice_generation"
    )

    graph.add_edge(
        "voice_generation",
        "media_generation"
    )

    graph.add_edge(
        "media_generation",
        END
    )

    return graph.compile()