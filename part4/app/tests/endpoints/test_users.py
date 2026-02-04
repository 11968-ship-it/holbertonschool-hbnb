import unittest
from app import create_app

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        
       # Login admin to get token
       login_resp = self.client.post('/api/v1/auth/login', json={
          "email": "admin@hbnb.io",
         "password": "admin1234"
       })
       self.admin_token = login_resp.get_json()['access_token']
    
    def test_create_user_success(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com",
            headers={"Authorization": f"Bearer {self.admin_token}"
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data["first_name"], "Jane")

    def test_create_user_failure(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "wrong-email"
        })
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()
