import requests
from infrastructure.ai.llm_base import LLMClient


class OllamaSummarizer(LLMClient):
    def __init__(self, model="mistral"):
        self.model = model
        self.url = "http://localhost:11434/api/generate"

    def summarize(self, text: str) -> str:
        # Limit input size (avoid huge prompt)
        trimmed_text = text[:3000]

        prompt = f"""
        You are a helpful assistant.
        Summarize the following book content in a clear and concise paragraph:

        {trimmed_text}
        """

        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            },
            timeout=300
        )

        response.raise_for_status()

        return response.json()["response"].strip()