from src.services.video_compiler_service import (
    VideoCompilerService
)


compiler = VideoCompilerService()


def compile_video(
    media_files: list,
    audio_path: str,
    width: int = 1920,
    height: int = 1080
) -> str:

    final_path = compiler.compile(
        media_files=media_files,
        audio_path=audio_path,
        width=width,
        height=height
    )

    return final_path