from app import db
from sqlalchemy.orm import validates
from app.models.base_model import BaseModel

class Review(BaseModel):
    __tablename__ = 'Review'
    __table_args__ = (
        db.UniqueConstraint('user_id', 'place_id', name='uq_review_user_place'),
    )

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    #FK columns
    place_id = db.Column(db.String(36), db.ForeignKey("Place.id"), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey("User.id"), nullable=False)

    # relationships
    place = db.relationship("Place", back_populates="reviews", lazy=True)
    user = db.relationship("User", back_populates="reviews", lazy=True)
    
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
            "place_id": self.place_id,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
