from app.models.base_model import BaseModel
from app import db
from app.models.place_amenity import place_amenity
from sqlalchemy.orm import validates, relationship


class Place(BaseModel):
    __tablename__ = 'Place'
    
    title = db.Column(db.String(100), nullable=False) #Title of the place.
    description = db.Column(db.Text, nullable=True) # Description of the place.
    price = db.Column(db.Float, nullable=False) # Price per night.
    latitude = db.Column(db.Float, nullable=False) # Latitude of the place.
    longitude = db.Column(db.Float, nullable=False) # Longitude of the place.

    # Foreign key to User
    owner_id = db.Column(db.String(36), db.ForeignKey('User.id'), nullable=False)
    
    # Relationships
    owner = relationship('User', back_populates='places')
    reviews = relationship('Review', back_populates='place', lazy=True, cascade='all, delete-orphan')
    amenities = relationship('Amenity', secondary=place_amenity, back_populates='places')

    # Validators
    @validates('title')
    def validate_title(self, key, value):
        """Validate title is not empty and within length."""
        if not isinstance(value, str):
            raise TypeError("Title must be a string")
        value = value.strip()
        if not value:
            raise ValueError("Title cannot be empty")
        if len(value) > 100:
            raise ValueError("Title must be at most 100 characters")
        return value

    @validates('price')
    def validate_price(self, key, value):
        """Validate price is positive."""
        if not isinstance(value, (int, float)):
            raise TypeError("Price must be a number")
        value = float(value)
        if value <= 0:
            raise ValueError("Price must be positive")
        return value

    @validates('latitude')
    def validate_latitude(self, key, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Latitude must be a number")
        value = float(value)
        if not -90.0 <= value <= 90.0:
            raise ValueError("Latitude must be within -90.0 to 90.0")
        return value

    @validates('longitude')
    def validate_longitude(self, key, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Longitude must be a number")
        value = float(value)
        if not -180.0 <= value <= 180.0:
            raise ValueError("Longitude must be within -180.0 to 180.0")
        return value

    def __repr__(self):
        return f"<Place '{self.title}' - ${self.price}/night>"
