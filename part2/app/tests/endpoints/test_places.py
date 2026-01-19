import unittest
import uuid
from app import create_app

class TestPlaceEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

        unique_email = f"john.{uuid.uuid4()}@example.com"

        user_resp = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": unique_email
        })
        self.assertEqual(user_resp.status_code, 201, msg=user_resp.get_data(as_text=True))
        self.user_id = user_resp.get_json()["id"]

    def test_create_place(self):
        resp = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "Nice place",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.user_id,
            "amenities": []
        })
        self.assertEqual(resp.status_code, 201, msg=resp.get_data(as_text=True))

    def test_create_place_invalid_owner(self):
        resp = self.client.post('/api/v1/places/', json={
            "title": "Invalid Place",
            "price": 100.0,
            "latitude": 0.0,
            "longitude": 0.0,
            "owner_id": "invalid-id",
            "amenities": []
        })
        self.assertEqual(resp.status_code, 400, msg=resp.get_data(as_text=True))

    def test_get_all_places(self):
        resp = self.client.get('/api/v1/places/')
        self.assertEqual(resp.status_code, 200, msg=resp.get_data(as_text=True))

    def test_get_place_by_id(self):
        place_resp = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "price": 50.0,
            "latitude": 10.0,
            "longitude": 10.0,
            "owner_id": self.user_id,
            "amenities": []
        })
        self.assertEqual(place_resp.status_code, 201, msg=place_resp.get_data(as_text=True))
        place_id = place_resp.get_json()["id"]

        resp = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(resp.status_code, 200, msg=resp.get_data(as_text=True))

    def test_update_place(self):
        place_resp = self.client.post('/api/v1/places/', json={
            "title": "Old Title",
            "price": 80.0,
            "latitude": 1.0,
            "longitude": 1.0,
            "owner_id": self.user_id,
            "amenities": []
        })
        self.assertEqual(place_resp.status_code, 201, msg=place_resp.get_data(as_text=True))
        place_id = place_resp.get_json()["id"]

        resp = self.client.put(f'/api/v1/places/{place_id}', json={
            "title": "New Title",
            "price": 120.0
        })
        self.assertEqual(resp.status_code, 200, msg=resp.get_data(as_text=True))

    def test_get_place_not_found(self):
        resp = self.client.get('/api/v1/places/non-existent-id')
        self.assertEqual(resp.status_code, 404, msg=resp.get_data(as_text=True))

if __name__ == "__main__":
    unittest.main()
