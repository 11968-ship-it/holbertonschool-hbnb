from app.models.base_model import BaseModel
from app import db, bcrypt
import uuid


class Place(BaseModel):
    __tablename__ = 'place'
    title = db.column(db.String(50), nullable=False) #Title of the place.
    description = db.column(db.Text, nullable=False) # Description of the place.
    price = db.column(db.Float, nullable=False) # Price per night.
    latitude = db.column(db.Float, nullable=False) # Latitude of the place.
    longitude = db.column(db.Float, nullable=False) # Longitude of the place.

        if self not in self.owner.places:
            self.owner.places.append(self)
        
    def add_review(self, review):
        """Add a review to the place."""
        from app.models.review import Review

        if not isinstance(review, Review):
            raise TypeError("review must be a Review instance")
        if review.place is not self:
            raise ValueError("review.place must reference this place")
        if review not in self.reviews:
            self.reviews.append(review)
            self.save()

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        from app.models.amenity import Amenity
        
        if not isinstance(amenity, Amenity):
            raise TypeError("amenity must be an Amenity instance")
        if amenity not in self.amenities:
            self.amenities.append(amenity)
            self.save()

    @staticmethod
    def _validate_title(value):
        if not isinstance(value, str):
            raise TypeError("Title must be a string!")
        value = value.strip()
        if not value:
            raise ValueError("Title is required!")
        if len(value) > 100:
            raise ValueError("Title must be at most 100 characters!")
        return value

    @staticmethod
    def _validate_description(value):
        if value is None:
            return ""
        if not isinstance(value, str):
            raise TypeError("Description must be a string!")
        return value.strip()

    @staticmethod
    def _validate_price(value):
        if not isinstance(value, (int, float)):
            raise TypeError("Price must be a number!")
        value = float(value)
        if value <= 0:
            raise ValueError("Price must be a positive value")
        return value

    @staticmethod
    def _validate_latitude(value):
        if not isinstance(value, (int, float)):
            raise TypeError("Latitude must be a number!")
        value = float(value)
        if value < -90.0 or value > 90.0:
            raise ValueError("Latitude must be within -90.0 to 90.0")
        return value

    @staticmethod
    def _validate_longitude(value):
        if not isinstance(value, (int, float)):
            raise TypeError("Longitude must be a number!")
        value = float(value)
        if value < -180.0 or value > 180.0:
            raise ValueError("Longitude must be within -180.0 to 180.0")
        return value

    @staticmethod
    def _validate_owner(value):
        if value is None:
            raise ValueError("Owner is required!")
        if not isinstance(value, User):
            raise TypeError("Owner must be a user instance")
        return value
