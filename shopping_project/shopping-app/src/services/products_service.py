from src.utils.database import get_db_connection

class ProductService:
    def __init__(self):
        self.connection = get_db_connection()

    def create_product(self, name, price):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO products (name, price) VALUES (?, ?)", (name, price))
            return cursor.lastrowid

    def get_product(self, product_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM products WHERE product_id = ?", (product_id,))
        return cursor.fetchone()

    def update_product(self, product_id, name, price):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute("UPDATE products SET name = ?, price = ? WHERE product_id = ?", (name, price, product_id))

    def delete_product(self, product_id):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM products WHERE product_id = ?", (product_id,))

    def get_all_products(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM products")
        return cursor.fetchall()