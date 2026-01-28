from app.models.review import Review
from app.persistence.repository import SQLAlchemyRepository


class ReviewRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Review)

    def get_by_rating(self, rating: int):
        return self.model.query.filter_by(rating=rating).all()

    def get_by_user_and_place(self, user_id, place_id):
    """Find review by user and place"""
    return self.model.query.filter_by(
        user_id=user_id,
        place_id=place_id
    ).first()
