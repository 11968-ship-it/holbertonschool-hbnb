from app.models.base_model import BaseModel
from app import db, bcrypt
from sqlalchemy.orm import validates


class Place(BaseModel):
    __tablename__ = 'places'
    
    title = db.Column(db.String(100), nullable=False) #Title of the place.
    description = db.Column(db.Text, nullable=True) # Description of the place.
    price = db.Column(db.Float, nullable=False) # Price per night.
    latitude = db.Column(db.Float, nullable=False) # Latitude of the place.
    longitude = db.Column(db.Float, nullable=False) # Longitude of the place.

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
            raise TypeError("Longitude must be a number!")
        value = float(value)
        if not -180.0 <= value <= 180.0:
            raise ValueError("Longitude must be within -180.0 to 180.0")
        return value
