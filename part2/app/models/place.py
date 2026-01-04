from app.models.base_model import BaseModel


class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)


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
    if not isinstance(value, (int, float):
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
