from infrastructure.db.connection import get_connection


class PostgresReviewRepository:
    def save(self, review: dict) -> dict:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO reviews (book_id, user_id, text, sentiment, created_at)
            VALUES (%s, %s, %s, %s, NOW())
            RETURNING *;
            """,
            (
                review["book_id"],
                review["user_id"],
                review["text"],
                review["sentiment"],
            ),
        )

        saved = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return dict(saved)

    def get_by_book_id(self, book_id: str):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM reviews WHERE book_id=%s;", (book_id,)
        )
        reviews = cur.fetchall()
        cur.close()
        conn.close()
        return list(reviews)

    def get_positive_reviews(self, user_id: int):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT * FROM reviews
            WHERE user_id=%s AND sentiment='Positive';
            """,
            (user_id,),
        )

        rows = cur.fetchall()

        cur.close()
        conn.close()

        return [dict(row) for row in rows]