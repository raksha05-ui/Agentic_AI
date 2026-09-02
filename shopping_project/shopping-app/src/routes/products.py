from flask import Blueprint, request, jsonify
from src.services.products_service import ProductsService

products_bp = Blueprint('products', __name__)
products_service = ProductsService()

@products_bp.route('/products', methods=['POST'])
def create_product():
    data = request.json
    product = products_service.create_product(data)
    return jsonify(product), 201

@products_bp.route('/products', methods=['GET'])
def get_products():
    products = products_service.get_all_products()
    return jsonify(products), 200

@products_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = products_service.get_product_by_id(product_id)
    if product:
        return jsonify(product), 200
    return jsonify({'error': 'Product not found'}), 404