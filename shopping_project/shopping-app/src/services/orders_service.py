from src.utils.database import get_db_connection

class OrderService:
    def __init__(self):
        self.connection = get_db_connection()

    def create_order(self, product_id, quantity):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO orders (product_id, quantity) VALUES (?, ?)",
                (product_id, quantity)
            )
            return cursor.lastrowid

    def get_order(self, order_id):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM orders WHERE order_id = ?",
            (order_id,)
        )
        return cursor.fetchone()

    def update_order(self, order_id, product_id, quantity):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(
                "UPDATE orders SET product_id = ?, quantity = ? WHERE order_id = ?",
                (product_id, quantity, order_id)
            )
            return cursor.rowcount

    def delete_order(self, order_id):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(
                "DELETE FROM orders WHERE order_id = ?",
                (order_id,)
            )
            return cursor.rowcount

    def get_all_orders(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM orders")
        return cursor.fetchall()