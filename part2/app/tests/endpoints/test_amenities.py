import unittest
from app import create_app

class TestAmenityEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_amenity_success(self):
        response = self.client.post('/api/v1/amenities/', json={"name": "Pool"})
        self.assertEqual(response.status_code, 201)

    def test_create_amenity_failure(self):
        response = self.client.post('/api/v1/amenities/', json={"name": ""})
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()
