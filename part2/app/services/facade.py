class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # --- Users ---
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute("email", email)

    def get_all_users(self):
        return self.user_repo.get_all()

    # --- Places ---
    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    # --- Reviews ---
    def create_review(self, review_data):
        text = review_data.get("text")
        rating = review_data.get("rating")
        user_id = review_data.get("user_id")
        place_id = review_data.get("place_id")

        # --- Validation ---
        if not text or not isinstance(rating, int):
            raise ValueError("Invalid review data")
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be 1-5")

        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("User not found")

        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")

        # --- Create review ---
        review = Review(text, rating, user_id, place_id)
        self.review_repo.add(review)

        # Attach review to place
        place.reviews.append(review)

        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        return place.reviews

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None

        if "text" in review_data:
            review.text = review_data["text"]

        if "rating" in review_data:
            rating = review_data["rating"]
            if rating < 1 or rating > 5:
                raise ValueError("Rating must be 1-5")
            review.rating = rating

        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return False

        # Remove from place
        place = self.place_repo.get(review.place_id)
        if place:
            place.reviews = [r for r in place.reviews if r.id != review_id]

        # Remove from repo
        self.review_repo.delete(review_id)
        return True
