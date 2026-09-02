class Review:
    def __init__(self, review_id, product_id, rating, comment):
        self.review_id = review_id
        self.product_id = product_id
        self.rating = rating
        self.comment = comment

    def create_review(self, db_connection):
        # Logic to create a review in the database
        pass

    def get_review(self, db_connection):
        # Logic to retrieve a review from the database
        pass

    @staticmethod
    def get_reviews_by_product(db_connection, product_id):
        # Logic to retrieve all reviews for a specific product
        pass