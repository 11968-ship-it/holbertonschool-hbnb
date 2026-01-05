from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

def test_user():
    user = User(first_name="John", last_name="Doe", email="john.doe@example.com")
    assert user.first_name == "John"
    assert user.is_admin is False
    print("User test passed!")

def test_place_and_relationships():
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
    place = Place(title="Cozy Apartment", description="Nice stay", price=100, latitude=37.7, longitude=-122.4, owner=owner)
    review = Review(text="Great!", rating=5, place=place, user=owner)
    place.add_review(review)
    wifi = Amenity(name="Wi-Fi")
    place.add_amenity(wifi)
    assert len(place.reviews) == 1
    assert place.amenities[0].name == "Wi-Fi"
    print("Place test passed!")

def test_review():
    user = User(first_name="Bob", last_name="Lee", email="bob@example.com")
    place = Place(title="Beach House", description="Sunny", price=200, latitude=34.0, longitude=-118.0, owner=user)
    review = Review(text="Loved it!", rating=4, place=place, user=user)
    assert review.rating == 4
    print("Review test passed!")

def test_amenity():
    amenity = Amenity(name="Parking")
    assert amenity.name == "Parking"
    print("Amenity test passed!")

if __name__ == "__main__":
    test_user()
    test_place_and_relationships()
    test_review()
    test_amenity()
