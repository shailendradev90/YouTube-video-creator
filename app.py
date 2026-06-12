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

format_options = {
    "YouTube Shorts / Instagram Reels (9:16)": {
        "width": 1080,
        "height": 1920,
        "orientation": "portrait"
    },
    "YouTube Long-form (16:9)": {
        "width": 1920,
        "height": 1080,
        "orientation": "landscape"
    },
    "Square Post (1:1)": {
        "width": 1080,
        "height": 1080,
        "orientation": "square"
    }
}

video_format = st.selectbox(
    "Video Format",
    list(format_options.keys())
)

selected_resolution = format_options[video_format]

if st.button("Generate Script"):

    with st.spinner(
        "Generating video... "
        "This may take a few minutes."
    ):

        graph = build_graph()

        result = graph.invoke(
            {
                "topic": topic,
                "language": language,
                "duration": duration,
                "style": style,
                "script": "",
                "audio_path": "",
                "media_files": [],
                "final_video": "",
                "video_width": selected_resolution["width"],
                "video_height": selected_resolution["height"],
                "orientation": selected_resolution["orientation"]
            }
        )

        script = result["script"]
        audio_path = result["audio_path"]

        st.success(
            "Video Generated Successfully!"
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

        st.subheader("🎬 Final Video")
        final_video = result["final_video"]
        st.video(final_video)

        with open(
            final_video, "rb"
        ) as video_file:
            st.download_button(
                "Download Video",
                video_file,
                file_name="final_video.mp4"
            )

        media_files = result["media_files"]
        st.info(
            f"{len(media_files)} clips used"
        )