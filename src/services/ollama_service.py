from langchain_ollama import ChatOllama
from src.config import OLLAMA_MODEL


class OllamaService:

    def __init__(self):
        self.llm = ChatOllama(
            model=OLLAMA_MODEL,
            temperature=0.7
        )

    def generate(self, prompt: str) -> str:
        response = self.llm.invoke(prompt)
        return response.content