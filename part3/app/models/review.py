from app import db
from sqlalchemy.orm import validates
from app.models.base_model import BaseModel

class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    
    @validates("text")
    def validate_text(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Review text must be a non-empty string")
        return value.strip()

    @validates("rating")
    def validate_rating(self, key, value):
        if not isinstance(value, int) or value < 1 or value > 5:
            raise ValueError("Rating must be an integer between 1 and 5")
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
