import requests


class OllamaEmbeddingService:
    def __init__(self, model="mistral"):
        self.model = model
        self.url = "http://localhost:11434/api/embeddings"

    def generate(self, text: str):
        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "prompt": text[:2000]  # limit size
            },
            timeout=300
        )

        response.raise_for_status()
        return response.json()["embedding"]