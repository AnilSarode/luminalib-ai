from abc import ABC, abstractmethod


class LLMClient(ABC):
    @abstractmethod
    def summarize(self, text: str) -> str:
        pass
