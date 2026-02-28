from dataclasses import dataclass
from datetime import datetime


# -----------------------------
# Command
# -----------------------------
@dataclass
class BorrowBookCommand:
    book_id: str
    user_id: int


# -----------------------------
# Repository Interfaces
# -----------------------------
class BookRepository:
    def get_by_id(self, book_id: str):
        raise NotImplementedError


class BorrowingRepository:
    def is_book_borrowed(self, book_id: str) -> bool:
        raise NotImplementedError

    def save(self, borrowing: dict) -> dict:
        raise NotImplementedError


# -----------------------------
# Use Case
# -----------------------------
class BorrowBookUseCase:
    def __init__(
        self,
        book_repository: BookRepository,
        borrowing_repository: BorrowingRepository,
    ):
        self.book_repository = book_repository
        self.borrowing_repository = borrowing_repository

    def execute(self, command: BorrowBookCommand) -> dict:
        # ---- Rule 1: Book must exist ----
        book = self.book_repository.get_by_id(command.book_id)
        if not book:
            raise ValueError("Book does not exist")

        # ---- Rule 2: Book must not be borrowed ----
        if self.borrowing_repository.is_book_borrowed(command.book_id):
            raise ValueError("Book is already borrowed")

        # ---- Create borrowing ----
        borrowing = {
            "book_id": command.book_id,
            "user_id": command.user_id,
            "borrowed_at": datetime.utcnow().isoformat(),
            "returned_at": None,
        }

        return self.borrowing_repository.save(borrowing)
