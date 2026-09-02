from src.services.product_assistant import ProductAssistant


PRODUCTS = [
    {"id": 1, "name": "Laptop", "description": "Lightweight laptop for work and study", "price": 899.99, "stock": 8},
    {"id": 2, "name": "Wireless Mouse", "description": "Ergonomic wireless mouse", "price": 29.99, "stock": 25},
    {"id": 3, "name": "Headphones", "description": "Noise-cancelling headphones", "price": 149.99, "stock": 0},
]

REVIEWS = [
    {"id": 1, "product_id": 1, "user_name": "Alice", "rating": 5, "comment": "Excellent battery life and performance."},
    {"id": 2, "product_id": 1, "user_name": "Bob", "rating": 4, "comment": "Very good but a bit heavy."},
    {"id": 3, "product_id": 2, "user_name": "Cara", "rating": 5, "comment": "Smooth and reliable."},
    {"id": 4, "product_id": 2, "user_name": "Drew", "rating": 2, "comment": "Battery is weak."},
]

ORDERS = [
    {"id": 1, "product_id": 1, "user_id": 101, "quantity": 2, "total_price": 1799.98, "status": "pending"},
    {"id": 2, "product_id": 2, "user_id": 102, "quantity": 1, "total_price": 29.99, "status": "completed"},
    {"id": 3, "product_id": 1, "user_id": 103, "quantity": 1, "total_price": 899.99, "status": "shipped"},
]


def test_price_question():
    assistant = ProductAssistant(PRODUCTS)
    answer = assistant.answer("What is the price of Laptop?")
    assert "899.99" in answer
    assert "Laptop" in answer


def test_show_all_products():
    assistant = ProductAssistant(PRODUCTS)
    answer = assistant.answer("Show me all products")
    assert "Laptop" in answer
    assert "Wireless Mouse" in answer
    assert "Headphones" in answer


def test_in_stock_question():
    assistant = ProductAssistant(PRODUCTS)
    answer = assistant.answer("Which products are in stock?")
    assert "Laptop" in answer
    assert "Wireless Mouse" in answer
    assert "Headphones" not in answer


def test_budget_question():
    assistant = ProductAssistant(PRODUCTS)
    answer = assistant.answer("Which products are under $50?")
    assert "Wireless Mouse" in answer
    assert "Laptop" not in answer


def test_review_summary_question():
    assistant = ProductAssistant(PRODUCTS, REVIEWS)
    answer = assistant.answer("How do customers feel about Laptop?")
    assert "4.5" in answer or "average" in answer.lower()
    assert "Excellent" in answer or "good" in answer.lower()


def test_review_count_question():
    assistant = ProductAssistant(PRODUCTS, REVIEWS)
    answer = assistant.answer("How many reviews does Wireless Mouse have?")
    assert "2" in answer
    assert "Wireless Mouse" in answer


def test_order_count_question():
    assistant = ProductAssistant(PRODUCTS, REVIEWS, ORDERS)
    answer = assistant.answer("How many orders are there?")
    assert "3" in answer


def test_order_status_question():
    assistant = ProductAssistant(PRODUCTS, REVIEWS, ORDERS)
    answer = assistant.answer("What is the status of the Laptop order?")
    assert "pending" in answer.lower() or "shipped" in answer.lower()
    assert "Laptop" in answer


def test_total_revenue_question():
    assistant = ProductAssistant(PRODUCTS, REVIEWS, ORDERS)
    answer = assistant.answer("What is the total revenue?")
    assert "2729.96" in answer or "total revenue" in answer.lower()
