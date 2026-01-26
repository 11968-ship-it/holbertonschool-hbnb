from app.models.base_model import BaseModel
from app import db
from sqlalchemy.orm import validates

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)

    @validates("name")
    def validate_name(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name is required")
        if len(value.strip()) > 50:
                    raise ValueError("Name must be under 50 characters")
        return value.strip()
