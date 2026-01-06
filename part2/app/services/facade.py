from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()


    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)
    
    # Placeholder method for fetching a place by ID
    def get_place(self, place_id):
       
        pass

    # need to change it a bit !!!
    
    def create_review(self, review_data):
        user = self.user_repo.get(review_data["user?"])

    def get_review(self, review_id):
        review = self.review_repo.get(review_id)
        return review
