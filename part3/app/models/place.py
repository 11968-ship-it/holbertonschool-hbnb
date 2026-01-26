from app.models.base_model import BaseModel
from app import db, bcrypt
import uuid


class Place(BaseModel):
    __tablename__ = 'place'
    
    title = db.Column(db.String(100), nullable=False) #Title of the place.
    description = db.Column(db.Text, nullable=False) # Description of the place.
    price = db.Column(db.Float, nullable=False) # Price per night.
    latitude = db.Column(db.Float, nullable=False) # Latitude of the place.
    longitude = db.Column(db.Float, nullable=False) # Longitude of the place.
