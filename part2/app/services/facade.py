from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

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

        self.place_repo.update(place)
        return place
        
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



    # --- Amenities ---
    def create_amenity(self, amenity_data):
        name = amenity_data.get("name")
        amenity = Amenity(name=name)
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
            amenity.name = amenity_data["name"]

        self.amenity_repo.update(amenity)
        return amenity
