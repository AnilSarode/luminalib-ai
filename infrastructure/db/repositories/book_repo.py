from infrastructure.db.connection import get_connection
from psycopg2.extras import Json

class PostgresBookRepository:
    def save(self, book: dict) -> dict:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO books (id, title, author, category, description, file_path)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING *;
            """,
            (
                book["id"],
                book["title"],
                book["author"],
                book["category"],
                book.get("description"),
                book.get("file_path"),
            ),
        )

        saved = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return dict(saved)

    def get_all(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM books;")
        books = cur.fetchall()
        cur.close()
        conn.close()
        return list(books)

    def get_by_id(self, book_id: str):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM books WHERE id=%s;", (book_id,))
        book = cur.fetchone()
        cur.close()
        conn.close()
        return dict(book) if book else None



    def update(self, book_id: str, data: dict):
        conn = get_connection()
        cur = conn.cursor()

        fields = []
        values = []

        for key in [
            "title",
            "author",
            "category",
            "description",
            "summary",
            "embedding",
        ]:
            if key in data:
                fields.append(f"{key}=%s")

                if key == "embedding":
                    values.append(Json(data[key]))  # important
                else:
                    values.append(data[key])

        if not fields:
            return self.get_by_id(book_id)

        values.append(book_id)

        cur.execute(
            f"""
            UPDATE books SET {', '.join(fields)}
            WHERE id=%s
            RETURNING *;
            """,
            values,
        )

        updated = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        return dict(updated) if updated else None

    def delete(self, book_id: str) -> bool:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM books WHERE id=%s;", (book_id,))
        deleted = cur.rowcount > 0
        conn.commit()
        cur.close()
        conn.close()
        return deleted
