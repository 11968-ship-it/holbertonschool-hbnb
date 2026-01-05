from app.models.base_model import BaseModel
from app.models.place import Place
from app.models.user import User

class Review(BaseModel):
    def __init__(self, text: str, rating: int, place: Place, user: User):
        super().__init__()

        # Validation
        if not text or not isinstance(text, str):
            raise ValueError("Review text must be a non-empty string")

        if not isinstance(rating, int) or rating < 1 or rating > 5:
            raise ValueError("Rating must be an integer between 1 and 5")

        if not place_id or not isinstance(place, Place):
            raise ValueError("place_id must be a valid string")

        if not user_id or not isinstance(user, User):
            raise ValueError("user_id must be a valid string")

        # Attributes
        self.text = text
        self.rating = rating
        self.place = Place
        self.user = User
