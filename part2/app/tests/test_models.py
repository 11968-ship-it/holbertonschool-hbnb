from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

# --- User Test ---
def test_user_creation():
    user = User(first_name="John", last_name="Doe", email="john.doe@example.com")
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example.com"
    assert user.is_admin is False
    print("✅ User creation test passed!")

# --- Place Test ---
def test_place_creation():
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
    place = Place(
        title="Cozy Apartment",
        description="A nice place to stay",
        price=100,
        latitude=37.7749,
        longitude=-122.4194,
        owner=owner
    )

    # Add a review
    review = Review(text="Great stay!", rating=5, place=place, user=owner)
    place.add_review(review)

    # Add an amenity
    wifi = Amenity(name="Wi-Fi")
    place.add_amenity(wifi)

    assert place.title == "Cozy Apartment"
    assert place.price == 100
    assert len(place.reviews) == 1
    assert place.reviews[0].text == "Great stay!"
    assert len(place.amenities) == 1
    assert place.amenities[0].name == "Wi-Fi"
    print("✅ Place creation and relationships test passed!")

# --- Amenity Test ---
def test_amenity_creation():
    amenity = Amenity(name="Parking")
    assert amenity.name == "Parking"
    print("✅ Amenity creation test passed!")

# --- Review Test ---
def test_review_creation():
    user = User(first_name="Bob", last_name="Lee", email="bob.lee@example.com")
    place = Place(
        title="Beach House",
        description="Sunny and nice",
        price=200,
        latitude=34.0,
        longitude=-118.0,
        owner=user
    )
    review = Review(text="Loved it!", rating=4, place=place, user=user)
    assert review.text == "Loved it!"
    assert review.rating == 4
    assert review.place == place
    assert review.user == user
    print("✅ Review creation test passed!")

# --- Run all tests ---
if __name__ == "__main__":
    test_user_creation()
    test_place_creation()
    test_amenity_creation()
    test_review_creation()
