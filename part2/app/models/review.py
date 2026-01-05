from models.base_model import BaseModel


class Review(BaseModel):
    def __init__(self, text, rating, place_id, user_id):
        super().__init__()

        # Validation
        if not text or not isinstance(text, str):
            raise ValueError("Review text must be a non-empty string")

        if not isinstance(rating, int) or rating < 1 or rating > 5:
            raise ValueError("Rating must be an integer between 1 and 5")

        if not place_id or not isinstance(place_id, str):
            raise ValueError("place_id must be a valid string")

        if not user_id or not isinstance(user_id, str):
            raise ValueError("user_id must be a valid string")

        # Attributes
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id
