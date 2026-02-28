from abc import ABC, abstractmethod


class FileStorage(ABC):
    @abstractmethod
    def save(self, file, filename: str) -> str:
        """
        Save file and return file path.
        """
        pass
