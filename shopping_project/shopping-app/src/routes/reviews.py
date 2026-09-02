from flask import Blueprint, request, jsonify
from src.services.reviews_service import ReviewsService

reviews_bp = Blueprint('reviews', __name__)
reviews_service = ReviewsService()

@reviews_bp.route('/reviews', methods=['POST'])
def create_review():
    data = request.json
    review = reviews_service.create_review(data)
    return jsonify(review), 201

@reviews_bp.route('/reviews/<int:review_id>', methods=['GET'])
def get_review(review_id):
    review = reviews_service.get_review(review_id)
    if review:
        return jsonify(review), 200
    return jsonify({'error': 'Review not found'}), 404

@reviews_bp.route('/reviews', methods=['GET'])
def get_reviews():
    reviews = reviews_service.get_all_reviews()
    return jsonify(reviews), 200