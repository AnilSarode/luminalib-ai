from dataclasses import dataclass
from typing import Optional
from uuid import uuid4
from datetime import datetime


# -----------------------------
# Input DTO
# -----------------------------
@dataclass
class AddBookCommand:
    title: str
    author: str
    category: str
    description: Optional[str] = None
    file_path: str | None = None

# -----------------------------
# Repository Interface
# -----------------------------
class BookRepository:
    """
    Abstract repository.
    Concrete implementation will be in infrastructure layer.
    """

    def save(self, book: dict) -> dict:
        raise NotImplementedError


# -----------------------------
# Use Case
# -----------------------------
class AddBookUseCase:
    def __init__(self, book_repository: BookRepository):
        self.book_repository = book_repository

    def execute(self, command: AddBookCommand) -> dict:
        # ---- Validation ----
        if not command.title:
            raise ValueError("Title is required")

        if not command.author:
            raise ValueError("Author is required")

        if not command.category:
            raise ValueError("Category is required")

        # ---- Create Book Entity ----
        book = {
            "id": str(uuid4()),
            "title": command.title,
            "author": command.author,
            "category": command.category,
            "description": command.description,
            "file_path": command.file_path,
            "created_at": datetime.utcnow().isoformat(),
        }

        # ---- Persist ----
        saved_book = self.book_repository.save(book)

        return saved_book
