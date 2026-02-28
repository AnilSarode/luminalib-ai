from flask import Blueprint, request, jsonify

from application.usecases.add_book import (
    AddBookCommand,
    AddBookUseCase,
)
from infrastructure.db.repositories.book_repo import PostgresBookRepository
from application.usecases.recommend_books import RecommendBooksUseCase
from infrastructure.db.repositories.review_repo import PostgresReviewRepository
from infrastructure.storage.local import LocalFileStorage

storage = LocalFileStorage()


books_bp = Blueprint("books", __name__)

# Repository instance (shared in memory)
book_repository = PostgresBookRepository()
review_repository = PostgresReviewRepository()


import threading
# from infrastructure.ai.summary_service import SimpleLLMClient
from application.usecases.summarize_book import SummarizeBookUseCase
from infrastructure.ai.summary_service import OllamaSummarizer

@books_bp.route("/books", methods=["POST"])
def add_book():
    try:
        title = request.form.get("title")
        author = request.form.get("author")
        category = request.form.get("category")
        description = request.form.get("description")

        uploaded_file = request.files.get("file")

        file_path = None
        if uploaded_file:
            file_path = storage.save(
                uploaded_file,
                uploaded_file.filename
            )

        command = AddBookCommand(
            title=title,
            author=author,
            category=category,
            description=description,
            file_path=file_path,
        )

        usecase = AddBookUseCase(book_repository)
        book = usecase.execute(command)

        # 2️⃣ Trigger async summary AFTER DB save
        if file_path:
            def run_summary():
                print("🔵 Background summarization started")
                summary_usecase = SummarizeBookUseCase(
                    book_repository=book_repository,
                    llm_client=OllamaSummarizer()   ,
                )
                summary_usecase.execute(book["id"], file_path)

                print("🟢 Background summarization finished")

            threading.Thread(target=run_summary).start()

        # 3️⃣ Respond immediately

        return jsonify(book), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400



@books_bp.route("/books", methods=["GET"])
def list_books():
    books = book_repository.get_all()
    return jsonify(books), 200


@books_bp.route("/books/<book_id>", methods=["GET"])
def get_book(book_id):
    book = book_repository.get_by_id(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    return jsonify(book), 200


@books_bp.route("/books/<book_id>", methods=["PUT"])
def update_book(book_id):
    data = request.json

    updated = book_repository.update(book_id, data)
    if not updated:
        return jsonify({"error": "Book not found"}), 404

    return jsonify(updated), 200


@books_bp.route("/books/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    deleted = book_repository.delete(book_id)
    if not deleted:
        return jsonify({"error": "Book not found"}), 404

    return jsonify({"message": "Book deleted successfully"}), 200

@books_bp.route("/users/<int:user_id>/recommendations", methods=["GET"])
def recommend_books(user_id):

    usecase = RecommendBooksUseCase(
        book_repository=book_repository,
        review_repository=review_repository,
    )

    recommendations = usecase.execute(user_id)

    return jsonify(recommendations), 200