from app.models.base_model import BaseModel


class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name

    @staticmethod
    def _validate_name(value):
        if not isinstance(value, str):
            raise TypeError "Name must be a string!"
        value = value.strip()
        if not value:
            raise ValueError "Name is required!"
        if len(value) > 50:
            raise ValueError "Name must be at most 50 characters!"
        return value
