from dataclasses import dataclass
from datetime import datetime
from infrastructure.ai.sentiment_service import OllamaSentimentAnalyzer

# -----------------------------
# Command
# -----------------------------
@dataclass
class AddReviewCommand:
    book_id: str
    user_id: int
    text: str


# -----------------------------
# Repository Interfaces
# -----------------------------
class BorrowingRepository:
    def has_user_borrowed(self, book_id: str, user_id: int) -> bool:
        raise NotImplementedError


class ReviewRepository:
    def save(self, review: dict) -> dict:
        raise NotImplementedError


# -----------------------------
# Use Case
# -----------------------------
class AddReviewUseCase:
    def __init__(
        self,
        borrowing_repository: BorrowingRepository,
        review_repository: ReviewRepository,
    ):
        self.borrowing_repository = borrowing_repository
        self.review_repository = review_repository
        self.sentiment_analyzer = OllamaSentimentAnalyzer()

    def execute(self, command: AddReviewCommand) -> dict:
        # ---- Validation ----
        if not command.text:
            raise ValueError("Review text is required")

        # ---- Rule: Must have borrowed ----
        if not self.borrowing_repository.has_user_borrowed(
            command.book_id, command.user_id
        ):
            raise ValueError("User must borrow the book before reviewing")

        sentiment = self.sentiment_analyzer.analyze(command.text)
        
        # ---- Create review ----
        review = {
            "book_id": command.book_id,
            "user_id": command.user_id,
            "text": command.text,
            "created_at": datetime.utcnow().isoformat(),
            "sentiment": sentiment,
        }

        return self.review_repository.save(review)
