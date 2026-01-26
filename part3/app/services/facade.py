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
        self.place_repo =  SQLAlchemyRepository(Place)
        self.review_repo =  SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

        
    
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

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        
        if "password" in user_data:
            password = user_data.pop("password")
            if not password or not str(password).strip():
                raise ValueError("Password is required")
            user.hash_password(password)

        for key, value in user_data.items():
            setattr(user, key, value)

        self.user_repo.update(user_id, user)
        return user

    # --- Places ---
    def create_place(self, place_data):
        required = ["title", "price", "latitude", "longitude", "owner_id", "amenities"]
        for key in required:
            if key not in place_data:
                raise ValueError(f"Missing required field: {key}")

        owner = self.user_repo.get(place_data["owner_id"])
        if not owner:
            raise ValueError("Owner not found")

        title = Place._validate_title(place_data["title"])
        description = Place._validate_description(place_data.get("description", ""))
        price = Place._validate_price(place_data["price"])
        latitude = Place._validate_latitude(place_data["latitude"])
        longitude = Place._validate_longitude(place_data["longitude"])

        amenity_objs = []
        for amenity_id in place_data.get("amenities", []):
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity not found: {amenity_id}")
            amenity_objs.append(amenity)

        place = Place(
            title=title,
            description=description,
            price=price,
            latitude=latitude,
            longitude=longitude,
            owner=owner
        )

        for a in amenity_objs:
            place.add_amenity(a)

        self.place_repo.add(place)
        return place
        
    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        if "owner_id" in place_data:
            owner = self.user_repo.get(place_data["owner_id"])
            if not owner:
                raise ValueError("Owner not found")
            place.owner = Place._validate_owner(owner)

        if "title" in place_data:
            place.title = Place._validate_title(place_data["title"])
        if "description" in place_data:
            place.description = Place._validate_description(place_data["description"])
        if "price" in place_data:
            place.price = Place._validate_price(place_data["price"])
        if "latitude" in place_data:
            place.latitude = Place._validate_latitude(place_data["latitude"])
        if "longitude" in place_data:
            place.longitude = Place._validate_longitude(place_data["longitude"])

        if "amenities" in place_data:
            amenity_objs = []
            for amenity_id in place_data["amenities"]:
                amenity = self.amenity_repo.get(amenity_id)
                if not amenity:
                    raise ValueError(f"Amenity not found: {amenity_id}")
                amenity_objs.append(amenity)

            place.amenities = []
            for a in amenity_objs:
                place.add_amenity(a)

        updated = self.place_repo.update(place_id, place_data)
        return updated if updated is not None else place
        
    # --- Reviews ---
    def create_review(self, review_data):
        text = review_data.get("text")
        rating = review_data.get("rating")

        # --- Validation ---
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Review text must be a non-empty string")
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            raise ValueError("Rating must be 1-5")
        
        # --- Create review ---
        review = Review(text=text.strip(), rating=rating)
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
        review = self.review_repo.delete(review_id)

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
