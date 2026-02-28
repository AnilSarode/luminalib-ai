from infrastructure.db.connection import get_connection
from datetime import datetime


class PostgresBorrowingRepository:
    def is_book_borrowed(self, book_id: str) -> bool:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT 1 FROM borrowings
            WHERE book_id=%s AND returned_at IS NULL;
            """,
            (book_id,),
        )
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result is not None

    def save(self, borrowing: dict) -> dict:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO borrowings (book_id, user_id, borrowed_at, returned_at)
            VALUES (%s, %s, %s, %s)
            RETURNING *;
            """,
            (
                borrowing["book_id"],
                borrowing["user_id"],
                borrowing["borrowed_at"],
                borrowing["returned_at"],
            ),
        )

        saved = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return dict(saved)

    def has_user_borrowed(self, book_id: str, user_id: int) -> bool:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT 1 FROM borrowings
            WHERE book_id=%s AND user_id=%s AND returned_at IS NULL;
            """,
            (book_id, user_id),
        )
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result is not None

    def return_book(self, book_id: str, user_id: int):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            UPDATE borrowings
            SET returned_at=%s
            WHERE book_id=%s AND user_id=%s AND returned_at IS NULL
            RETURNING *;
            """,
            (datetime.utcnow(), book_id, user_id),
        )

        updated = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return dict(updated) if updated else None
