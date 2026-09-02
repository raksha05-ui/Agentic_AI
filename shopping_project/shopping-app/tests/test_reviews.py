import pytest
from src.models.review import Review
from src.services.reviews_service import ReviewsService

@pytest.fixture
def review_data():
    return {
        "product_id": 1,
        "rating": 5,
        "comment": "Excellent product!"
    }

def test_create_review(review_data):
    review = ReviewsService.create_review(**review_data)
    assert review.review_id is not None
    assert review.product_id == review_data["product_id"]
    assert review.rating == review_data["rating"]
    assert review.comment == review_data["comment"]

def test_get_review(review_data):
    review = ReviewsService.create_review(**review_data)
    fetched_review = ReviewsService.get_review(review.review_id)
    assert fetched_review.review_id == review.review_id
    assert fetched_review.product_id == review_data["product_id"]
    assert fetched_review.rating == review_data["rating"]
    assert fetched_review.comment == review_data["comment"]

def test_get_reviews_for_product(review_data):
    ReviewsService.create_review(**review_data)
    reviews = ReviewsService.get_reviews_for_product(review_data["product_id"])
    assert len(reviews) > 0
    assert all(review.product_id == review_data["product_id"] for review in reviews)