from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    #--- user ---
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)
    
    # Placeholder method for fetching a place by ID
    #--- Place ---
    def get_place(self, place_id):
       
        pass

    #--- Review ---
    def create_review(self, review_data):
        text = review_data.get("text")
        rating = review_data.get("rating")
        user_id = review_data.get("user_id")
        place_id = review_data.get("place_id")

        review = Review(text, rating, user_id, place_id)
        self.reviews[review.id] = review

        self.places[place_id].reviews.append(review)
        return review

          def get_review(self, review_id):
        return self.reviews.get(review_id)

    def get_all_reviews(self):
        return list(self.reviews.values())

    def get_reviews_by_place(self, place_id):
        place = self.places.get(place_id)
        if not place:
            return None
        return place.reviews

    def update_review(self, review_id, review_data):
        review = self.reviews.get(review_id)
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
        review = self.reviews.pop(review_id, None)
        if not review:
            return False
            
        place = self.places.get(review.place_id)
        if place:
            place.reviews = [
                r for r in place.reviews if r.id != review_id
            ]

        return True
        

    #--- amenities ---
    def 
