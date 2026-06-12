import os
from moviepy import (
    VideoFileClip,
    AudioFileClip,
    concatenate_videoclips,
    vfx
)

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


class VideoCompilerService:

    def compile(
        self,
        media_files: list,
        audio_path: str,
        output_path: str = None,
        width: int = 1920,
        height: int = 1080
    ) -> str:

        if output_path is None:
            output_path = os.path.join(
                BASE_DIR,
                "output",
                "media",
                "videos",
                "final_video.mp4"
            )

        os.makedirs(
            os.path.dirname(output_path),
            exist_ok=True
        )

        audio_clip = AudioFileClip(audio_path)
        audio_duration = audio_clip.duration

        clips = []
        for file in media_files:
            abs_path = os.path.abspath(file)
            if os.path.exists(abs_path):
                try:
                    clip = VideoFileClip(abs_path)
                    resized = self._resize_clip(
                        clip, width, height
                    )
                    clips.append(resized)
                except Exception as e:
                    print(
                        f"Skipping {abs_path}: {e}"
                    )
                    continue
            else:
                print(
                    f"File not found: {abs_path}"
                )

        if not clips:
            raise RuntimeError(
                "No valid video clips found"
            )

        total_clip_duration = sum(
            c.duration for c in clips
        )

        if total_clip_duration < audio_duration:
            loops_needed = int(
                audio_duration
                / total_clip_duration
            ) + 1
            expanded = []
            for _ in range(loops_needed):
                expanded.extend(clips)
            clips = expanded

        trimmed_clips = []
        elapsed = 0
        for clip in clips:
            if elapsed >= audio_duration:
                break
            remaining = audio_duration - elapsed
            if clip.duration > remaining:
                clip = clip.subclipped(
                    0, remaining
                )
            trimmed_clips.append(clip)
            elapsed += clip.duration

        final_video = concatenate_videoclips(
            trimmed_clips,
            method="compose"
        )
        final_video = final_video.with_audio(
            audio_clip
        )

        final_video.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            fps=24,
            logger=None
        )

        for clip in trimmed_clips:
            clip.close()
        audio_clip.close()
        final_video.close()

        return output_path

    def _resize_clip(
        self, clip, target_w, target_h
    ):
        clip_w, clip_h = clip.size
        target_ratio = target_w / target_h
        clip_ratio = clip_w / clip_h

        if clip_ratio > target_ratio:
            new_w = int(clip_h * target_ratio)
            x_center = clip_w / 2
            clip = clip.cropped(
                x1=x_center - new_w / 2,
                x2=x_center + new_w / 2
            )
        elif clip_ratio < target_ratio:
            new_h = int(clip_w / target_ratio)
            y_center = clip_h / 2
            clip = clip.cropped(
                y1=y_center - new_h / 2,
                y2=y_center + new_h / 2
            )

        clip = clip.resized(
            new_size=(target_w, target_h)
        )

        return clip