import os
from infrastructure.storage.base import FileStorage


class LocalFileStorage(FileStorage):
    def __init__(self, base_path: str = "uploaded_books"):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

    def save(self, file, filename: str) -> str:
        file_path = os.path.join(self.base_path, filename)

        file.save(file_path)

        return file_path
