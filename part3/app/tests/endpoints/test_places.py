import unittest
from app import create_app

class TestPlaceEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        # Create a user to act as owner
        user_resp = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        })
        self.assertEqual(user_resp.status_code, 201)
        self.user_id = user_resp.get_json()["id"]

    def test_create_place(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "Nice place",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.user_id,
            "amenities": []
        })
        self.assertEqual(response.status_code, 201)

    def test_create_place_invalid_owner(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Invalid Place",
            "price": 100.0,
            "latitude": 0.0,
            "longitude": 0.0,
            "owner_id": "invalid-id",
            "amenities": []
        })
        self.assertEqual(response.status_code, 400)

    def test_get_all_places(self):
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)

    def test_get_place_by_id(self):
        # Create place first
        place_resp = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "price": 50.0,
            "latitude": 10.0,
            "longitude": 10.0,
            "owner_id": self.user_id,
            "amenities": []
        })
        place_id = place_resp.get_json()["id"]

        response = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(response.status_code, 200)

    def test_update_place(self):
        # Create place
        place_resp = self.client.post('/api/v1/places/', json={
            "title": "Old Title",
            "price": 80.0,
            "latitude": 1.0,
            "longitude": 1.0,
            "owner_id": self.user_id,
            "amenities": []
        })
        place_id = place_resp.get_json()["id"]

        # Update place
        response = self.client.put(f'/api/v1/places/{place_id}', json={
            "title": "New Title",
            "price": 120.0
        })
        self.assertEqual(response.status_code, 200)

    def test_get_place_not_found(self):
        response = self.client.get('/api/v1/places/non-existent-id')
        self.assertEqual(response.status_code, 404)
