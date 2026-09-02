import sys

sys.path.insert(0, r"C:\Users\user\Desktop\agentic_ai\shopping_project\shopping-app")

from src.services.product_assistant import ProductAssistant

PRODUCTS = [
    {"id": 1, "name": "Laptop", "description": "Lightweight laptop for work and study", "price": 899.99, "stock": 8},
    {"id": 2, "name": "Wireless Mouse", "description": "Ergonomic wireless mouse", "price": 29.99, "stock": 25},
    {"id": 3, "name": "Headphones", "description": "Noise-cancelling headphones", "price": 149.99, "stock": 0},
]

a = ProductAssistant(PRODUCTS)
assert "899.99" in a.answer("What is the price of Laptop?")
assert "Laptop" in a.answer("Show me all products")
assert "Headphones" not in a.answer("Which products are in stock?")
assert "Wireless Mouse" in a.answer("Which products are under $50?")
print("assistant_ok")
