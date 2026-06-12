from src.services.piper_service import PiperService

piper = PiperService()


def generate_voice(script: str) -> str:

    audio_path = piper.synthesize(script)

    return audio_path