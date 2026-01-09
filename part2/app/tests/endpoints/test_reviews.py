import unittest
import uuid
from app import create_app

class TestReviewEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

        # Create user (unique email each test)
        email = f"review.{uuid.uuid4()}@example.com"
        user_resp = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": email
        })
        self.assertEqual(user_resp.status_code, 201, msg=user_resp.get_data(as_text=True))
        self.user_id = user_resp.get_json()["id"]

        # Create place for place_id
        place_resp = self.client.post('/api/v1/places/', json={
            "title": "Review Place",
            "description": "Used for review tests",
            "price": 50.0,
            "latitude": 1.0,
            "longitude": 1.0,
            "owner_id": self.user_id,
            "amenities": []
        })
        self.assertEqual(place_resp.status_code, 201, msg=place_resp.get_data(as_text=True))
        self.place_id = place_resp.get_json()["id"]

    def test_create_review_success(self):
        resp = self.client.post('/api/v1/reviews/', json={
            "text": "Great place!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(resp.status_code, 201, msg=resp.get_data(as_text=True))
        data = resp.get_json()
        self.assertIn("id", data)
        self.assertEqual(data["text"], "Great place!")
        self.assertEqual(data["rating"], 5)

    def test_create_review_failure(self):
        resp = self.client.post('/api/v1/reviews/', json={
            "text": "",
            "rating": 10,
            "user_id": "wrong",
            "place_id": "wrong"
        })
        self.assertEqual(resp.status_code, 400, msg=resp.get_data(as_text=True))

    def test_update_review(self):
        # Create review first
        create = self.client.post('/api/v1/reviews/', json={
            "text": "Original",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(create.status_code, 201, msg=create.get_data(as_text=True))
        review_id = create.get_json()["id"]

        update = self.client.put(f'/api/v1/reviews/{review_id}', json={
            "text": "Updated",
            "rating": 4,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(update.status_code, 200, msg=update.get_data(as_text=True))

        # Confirm updated (GET)
        get = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(get.status_code, 200, msg=get.get_data(as_text=True))
        self.assertEqual(get.get_json()["text"], "Updated")
        self.assertEqual(get.get_json()["rating"], 4)

    def test_delete_review(self):
        # Create review first
        create = self.client.post('/api/v1/reviews/', json={
            "text": "To delete",
            "rating": 3,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(create.status_code, 201, msg=create.get_data(as_text=True))
        review_id = create.get_json()["id"]

        # Delete
        delete = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(delete.status_code, 200, msg=delete.get_data(as_text=True))

        # Confirm it's gone
        get = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(get.status_code, 404, msg=get.get_data(as_text=True))

    def test_update_review_not_found(self):
        resp = self.client.put('/api/v1/reviews/non-existent-id', json={
            "text": "Updated",
            "rating": 4,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(resp.status_code, 404, msg=resp.get_data(as_text=True))

    def test_delete_review_not_found(self):
        resp = self.client.delete('/api/v1/reviews/non-existent-id')
        self.assertEqual(resp.status_code, 404, msg=resp.get_data(as_text=True))

if __name__ == "__main__":
    unittest.main()
