from app.models.amenity import Amenity
from app.persistence.repository import SQLAlchemyRepository

class AmenityRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Amenity)

    def get_by_name(self, name: str):
        if not isinstance(name, str):
            return None
        return self.model.query.filter_by(name=name.strip()).first()
