from app.models.base_model import BaseModel
from app.models.place import Place
from app.models.user import User

class Review(BaseModel):
    def __init__(self, text: str, rating: int, place: place, user: user):
        super().__init__()
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Review text must be a non-empty string")
            
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            raise ValueError("Rating must be an integer between 1 and 5")
            
        if not isinstance(place, place):
            raise TypeError("place must be a Place instance")
            
        if not isinstance(user, user):
            raise TypeError("user must be a User instance")

        # Attributes
        self.text = text.strip()
        self.rating = rating
        self.place = place
        self.user = user
