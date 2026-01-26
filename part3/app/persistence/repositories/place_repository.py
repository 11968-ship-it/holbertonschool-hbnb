from app.models.place import Place 
from app import db
from app.persistence.repository import SQLAlchemyRepository

class PlaceRepository(SQLAlchemyRepository):
    """Repository for Place entity with place-specific operations."""
	def __init__(self):
		super().__init__(Place)
		
	def get_by_price_range(self, min_price, max_price):
		"""Find places within a specific price range."""
		return self.model.query.filter(
			self.model.price >= min_price,
            self.model.price <= max_price
		).all()
		
	def get_by_title(self, title):
        """Find a place by exact title match."""
        return self.model.query.filter_by(title=title).first()
		
	def search_by_title(self, keyword):
        """Search places with titles containing the keyword."""
        return self.model.query.filter(
            self.model.title.ilike(f'%{keyword}%')
        ).all()




    
