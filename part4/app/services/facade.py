from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.persistence.repositories.user_repository import UserRepository
from app.persistence.repositories.place_repository import PlaceRepository
from app.persistence.repositories.review_repository import ReviewRepository
from app.persistence.repositories.amenity_repository import AmenityRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

        
    
    # --- Users ---
    def create_user(self, user_data):
        user = User(**user_data)
        user.hash_password(user_data['password'])
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)

    def get_all_users(self):
        return self.user_repo.get_all()


    # update the user
    def update_user(self, user_id, user_data):
        # get the user from the repo
        user = self.user_repo.get(user_id)
        if not user:
            return None

        # Handle password separately
        if "password" in user_data:
            password = user_data.pop("password")
            if not password or not str(password).strip():
                raise ValueError("Password is required")
            user.hash_password(password)
            
        for key, value in user_data.items():
            setattr(user, key, value)

        # Update using repository
        # pass dictionary
        updated_user = self.user_repo.update(user_id, user_data)
        return updated_user
    
    # --- Places ---
    def create_place(self, place_data):
        """ Create a new place"""

        place_data_clean = {
            'title': place_data['title'],
            'description': place_data.get('description', ''),
            'location': place_data['location'],
            'price': place_data['price'],
            'latitude': place_data['latitude'],
            'longitude': place_data['longitude'],
            'owner_id': place_data['owner_id'],
        }

        place = Place(**place_data_clean)
        self.place_repo.add(place)
        return place
        
    def get_place(self, place_id):
        """get place by id"""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """get all place"""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """update place data"""
        place = self.place_repo.get(place_id)
        if not place:
            return None

        updated = self.place_repo.update(place_id, place_data)
        return updated if updated is not None else place

    def delete_place(self, place_id):
        """Delete a place."""
        place = self.place_repo.get(place_id)
        if not place:
            return False
        return self.place_repo.delete(place_id)

    def get_places_by_price_range(self, min_price, max_price):
        """Get places within price range."""
        return self.place_repo.get_by_price_range(min_price, max_price)

    def search_places_by_title(self, keyword):
        """Search places by title keyword."""
        return self.place_repo.search_by_title(keyword)
        
    # --- Reviews ---
    def create_review(self, review_data):
        text = review_data.get("text")
        rating = review_data.get("rating")
        place_id = review_data.get("place_id")
        user_id = review_data.get("user_id")

        # --- Validation ---
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Review text must be a non-empty string")
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            raise ValueError("Rating must be 1-5")
        if not place_id:
            raise ValueError("place_id is required")
        if not user_id:
            raise ValueError("user_id is required")

        if not self.place_repo.get(place_id):
            raise ValueError("Place not found")
        if not self.user_repo.get(user_id):
            raise ValueError("User not found")
        
        # --- Create review ---
        review = Review(
            text=text.strip(),
            rating=rating,
            place_id=place_id,
            user_id=user_id,
        )
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None

        if "text" in review_data:
            if not isinstance(review_data["text"], str) or not review_data["text"].strip():
                raise ValueError("Review text must be a non-empty string")

        if "rating" in review_data:
            rating = review_data["rating"]
            if not isinstance(rating, int) or rating < 1 or rating > 5:
                raise ValueError("Rating must be 1-5")
        
        updated = self.review_repo.update(review_id, review_data)
        return updated if updated is not None else review

    def delete_review(self, review_id):
        return self.review_repo.delete(review_id)

    def get_review_by_user_and_place(self, user_id, place_id):
        return self.review_repo.get_by_user_and_place(user_id, place_id)

    # --- Amenities ---
    def create_amenity(self, amenity_data):
        name = amenity_data.get("name")

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name is required")
        if len(name.strip()) > 50:
            raise ValueError("Name must be under 50 characters")

        # optional duplicate guard
        if self.amenity_repo.get_by_name(name):
            raise ValueError("Amenity already exists")

        amenity = Amenity(name=name.strip())
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None

        if "name" in amenity_data:
            name = amenity_data["name"]
            if not isinstance(name, str) or not name.strip():
                raise ValueError("Name is required")
            if len(name.strip()) > 50:
                raise ValueError("Name must be under 50 characters")

        updated = self.amenity_repo.update(amenity_id, amenity_data)
        return updated if updated is not None else amenity

    def delete_amenity(self, amenity_id):
        return self.amenity_repo.delete(amenity_id)
