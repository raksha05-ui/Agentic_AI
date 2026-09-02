from src.utils.database import get_db_connection

class ReviewService:
    def __init__(self):
        self.connection = get_db_connection()

    def create_review(self, product_id, rating, comment):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO reviews (product_id, rating, comment) VALUES (?, ?, ?)",
                (product_id, rating, comment)
            )
            return cursor.lastrowid

    def get_reviews_by_product(self, product_id):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM reviews WHERE product_id = ?",
            (product_id,)
        )
        return cursor.fetchall()

    def update_review(self, review_id, rating, comment):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(
                "UPDATE reviews SET rating = ?, comment = ? WHERE review_id = ?",
                (rating, comment, review_id)
            )
            return cursor.rowcount

    def delete_review(self, review_id):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(
                "DELETE FROM reviews WHERE review_id = ?",
                (review_id,)
            )
            return cursor.rowcount