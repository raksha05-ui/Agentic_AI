from flask import Blueprint, request, jsonify
from src.services.orders_service import create_order, get_orders

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/orders', methods=['POST'])
def create_order_route():
    data = request.json
    order = create_order(data)
    return jsonify(order), 201

@orders_bp.route('/orders', methods=['GET'])
def get_orders_route():
    orders = get_orders()
    return jsonify(orders), 200