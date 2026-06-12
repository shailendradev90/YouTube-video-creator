from src.services.ollama_service import OllamaService

ollama = OllamaService()


def generate_script(
        topic: str,
        duration: str,
        language: str,
        style: str
):

    prompt = f"""
You are an expert YouTube content creator.

Create a YouTube script.

Topic:
{topic}

Duration:
{duration}

Language:
{language}

Style:
{style}

Requirements:

1. Strong hook
2. Engaging storytelling
3. Easy language
4. Clear ending
5. CTA at end

Return only narration.
"""

    return ollama.generate(prompt)