import unittest
import uuid
from app import create_app

class TestReviewEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

        # Create a user first (unique email each run)
        email = f"review.{uuid.uuid4()}@example.com"
        user_resp = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": email
        })
        self.assertEqual(user_resp.status_code, 201, msg=user_resp.get_data(as_text=True))
        self.user_id = user_resp.get_json()["id"]

        # Create a place owned by that user
        place_resp = self.client.post('/api/v1/places/', json={
            "title": "Review Place",
            "description": "Place used for reviews testing",
            "price": 50.0,
            "latitude": 1.0,
            "longitude": 1.0,
            "owner_id": self.user_id,
            "amenities": []
        })
        self.assertEqual(place_resp.status_code, 201, msg=place_resp.get_data(as_text=True))
        self.place_id = place_resp.get_json()["id"]

    def test_create_review_success(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 201, msg=response.get_data(as_text=True))

    def test_create_review_failure(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "",
            "rating": 10,
            "user_id": "wrong",
            "place_id": "wrong"
        })
        self.assertEqual(response.status_code, 400, msg=response.get_data(as_text=True))

if __name__ == "__main__":
    unittest.main()
