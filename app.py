import streamlit as st

from src.workflow.video_graph import build_graph

st.set_page_config(
    page_title="AI Video Generator",
    layout="wide"
)

st.title("🎬 AI Faceless Video Generator")

topic = st.text_input(
    "Video Topic"
)

language = st.selectbox(
    "Language",
    ["English", "Hindi"]
)

duration = st.selectbox(
    "Duration",
    [
        "60 seconds",
        "3 minutes",
        "5 minutes",
        "10 minutes"
    ]
)

style = st.selectbox(
    "Style",
    [
        "Educational",
        "Storytelling",
        "Professional",
        "Motivational"
    ]
)

if st.button("Generate Script"):

    with st.spinner(
        "Generating script..."
    ):

        graph = build_graph()

        result = graph.invoke(
            {
                "topic": topic,
                "language": language,
                "duration": duration,
                "style": style,
                "script": ""
            }
        )

        script = result["script"]

        st.success(
            "Script Generated"
        )

        st.text_area(
            "Generated Script",
            script,
            height=500
        )

        st.download_button(
            "Download Script",
            script,
            file_name="youtube_script.txt"
        )