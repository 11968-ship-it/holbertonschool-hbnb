import unittest
from app import create_app

class TestReviewEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_review_success(self):
        # Replace with real user_id and place_id from your DB setup
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place!",
            "user_id": "some-user-id",
            "place_id": "some-place-id"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_review_failure(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "",
            "user_id": "wrong",
            "place_id": "wrong"
        })
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()
