from flask import Blueprint, jsonify
from datetime import datetime

from application.usecases.borrow_book import (
    BorrowBookCommand,
    BorrowBookUseCase,
)
from infrastructure.db.repositories.borrowing_repo import (
    PostgresBorrowingRepository,
)
from infrastructure.db.repositories.book_repo import PostgresBookRepository

borrowings_bp = Blueprint("borrowings", __name__)

# Shared repositories
borrowing_repository = PostgresBorrowingRepository()
book_repository = PostgresBookRepository()

MOCK_USER_ID = 1


@borrowings_bp.route("/books/<book_id>/borrow", methods=["POST"])
def borrow_book(book_id):
    try:
        command = BorrowBookCommand(
            book_id=book_id,
            user_id=MOCK_USER_ID,
        )

        usecase = BorrowBookUseCase(
            book_repository=book_repository,
            borrowing_repository=borrowing_repository,
        )

        borrowing = usecase.execute(command)
        return jsonify(borrowing), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@borrowings_bp.route("/books/<book_id>/return", methods=["POST"])
def return_book(book_id):
    borrowing = borrowing_repository.return_book(
        book_id=book_id,
        user_id=MOCK_USER_ID,
    )

    if not borrowing:
        return jsonify({"error": "No active borrowing found"}), 400

    borrowing["returned_at"] = datetime.utcnow().isoformat()
    return jsonify(borrowing), 200
