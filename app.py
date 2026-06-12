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
        "Generating script and audio..."
    ):

        graph = build_graph()

        result = graph.invoke(
            {
                "topic": topic,
                "language": language,
                "duration": duration,
                "style": style,
                "script": "",
                "audio_path": ""
            }
        )

        script = result["script"]
        audio_path = result["audio_path"]

        st.success(
            "Script and Audio Generated"
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

        st.audio(audio_path)

        with open(
            audio_path,
            "rb"
        ) as file:

            st.download_button(
                "Download Audio",
                file,
                file_name="narration.wav"
            )

        media_files = result["media_files"]
        st.success(
            f"{len(media_files)} clips downloaded"
        )
        for clip in media_files:
            st.video(clip)
