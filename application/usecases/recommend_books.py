from domain.services.recommendation_engine import cosine_similarity
import numpy as np


class RecommendBooksUseCase:
    def __init__(self, book_repository, review_repository):
        self.book_repository = book_repository
        self.review_repository = review_repository

    def execute(self, user_id: int):

        # 1️⃣ Get positively reviewed books
        positive_reviews = self.review_repository.get_positive_reviews(user_id)

        if not positive_reviews:
            return []

        # 2️⃣ Collect embeddings of liked books
        liked_embeddings = []

        for review in positive_reviews:
            book = self.book_repository.get_by_id(review["book_id"])
            if book["embedding"]:
                liked_embeddings.append(book["embedding"])

        if not liked_embeddings:
            return []

        # 3️⃣ Create user profile embedding (average vector)
        user_embedding = np.mean(liked_embeddings, axis=0)

        # 4️⃣ Compare with all books
        all_books = self.book_repository.get_all()

        scored_books = []

        for book in all_books:
            if not book["embedding"]:
                continue

            score = cosine_similarity(user_embedding, book["embedding"])

            scored_books.append((score, book))

        # 5️⃣ Sort by similarity
        scored_books.sort(reverse=True, key=lambda x: x[0])

        # Return top 5

        recommended = []

        for _, book in scored_books[:5]:
            book_copy = book.copy()
            book_copy.pop("embedding", None)
            recommended.append(book_copy)

        return recommended