import os
import subprocess
import tempfile


class PiperService:

    def __init__(
        self,
        model=None
    ):
        if model is None:
            base_dir = os.path.dirname(
                os.path.dirname(
                    os.path.dirname(
                        os.path.abspath(__file__)
                    )
                )
            )
            model = os.path.join(
                base_dir,
                "models",
                "en_US-lessac-medium.onnx"
            )
        self.model = model

    def synthesize(
        self,
        text: str,
        output_path: str = None
    ) -> str:

        if output_path is None:
            output_path = os.path.join(
                tempfile.gettempdir(),
                "narration.wav"
            )

        command = [
            "piper",
            "--model",
            self.model,
            "--output_file",
            output_path
        ]

        try:
            subprocess.run(
                command,
                input=text,
                text=True,
                check=True,
                capture_output=True
            )
        except FileNotFoundError:
            raise RuntimeError(
                "Piper TTS is not installed. "
                "Install it with: "
                "pip install piper-tts"
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"Piper TTS failed: {e.stderr}"
            )

        return output_path