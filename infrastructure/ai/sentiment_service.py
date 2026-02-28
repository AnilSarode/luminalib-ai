import requests
from infrastructure.ai.llm_base import LLMClient


class OllamaSentimentAnalyzer:
    def __init__(self, model="mistral"):
        self.model = model
        self.url = "http://localhost:11434/api/generate"

    def analyze(self, text: str) -> str:
        prompt = f"""
        Analyze the sentiment of the following review.
        Respond with ONLY one word: Positive, Neutral, or Negative.

        Review:
        {text}
        """

        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()
        result = response.json()["response"].strip()

        # Clean result (LLMs sometimes add extra text)
        result = result.split()[0].capitalize()

        if result not in ["Positive", "Neutral", "Negative"]:
            return "Neutral"

        return result