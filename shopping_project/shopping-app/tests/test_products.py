import pytest
from src.models.product import Product
from src.utils.database import connect_db

@pytest.fixture
def db_connection():
    connection = connect_db('data/store.db')
    yield connection
    connection.close()

def test_create_product(db_connection):
    product = Product(name="Test Product", price=9.99)
    product.create(db_connection)
    
    retrieved_product = Product.get_by_id(db_connection, product.product_id)
    assert retrieved_product.name == "Test Product"
    assert retrieved_product.price == 9.99

def test_get_all_products(db_connection):
    products = Product.get_all(db_connection)
    assert isinstance(products, list)

def test_update_product(db_connection):
    product = Product(name="Update Product", price=19.99)
    product.create(db_connection)
    
    product.price = 14.99
    product.update(db_connection)
    
    updated_product = Product.get_by_id(db_connection, product.product_id)
    assert updated_product.price == 14.99

def test_delete_product(db_connection):
    product = Product(name="Delete Product", price=29.99)
    product.create(db_connection)
    
    product.delete(db_connection)
    deleted_product = Product.get_by_id(db_connection, product.product_id)
    assert deleted_product is None