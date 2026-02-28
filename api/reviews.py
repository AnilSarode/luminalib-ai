from flask import Blueprint, request, jsonify

from application.usecases.add_review import (
    AddReviewCommand,
    AddReviewUseCase,
)
from infrastructure.db.repositories.review_repo import (
    PostgresReviewRepository,
)
from infrastructure.db.repositories.borrowing_repo import (
    PostgresBorrowingRepository,
)

reviews_bp = Blueprint("reviews", __name__)

# Shared repositories
review_repository = PostgresReviewRepository()
borrowing_repository = PostgresBorrowingRepository()

MOCK_USER_ID = 1


@reviews_bp.route("/books/<book_id>/reviews", methods=["POST"])
def add_review(book_id):
    data = request.json

    try:
        command = AddReviewCommand(
            book_id=book_id,
            user_id=MOCK_USER_ID,
            text=data.get("text"),
        )

        usecase = AddReviewUseCase(
            borrowing_repository=borrowing_repository,
            review_repository=review_repository,
        )

        review = usecase.execute(command)
        return jsonify(review), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@reviews_bp.route("/books/<book_id>/reviews", methods=["GET"])
def list_reviews(book_id):
    reviews = review_repository.get_by_book_id(book_id)
    return jsonify(reviews), 200
