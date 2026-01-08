import unittest
from app import create_app

class TestAmenityEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config.update(TESTING=True)
        self.client = self.app.test_client()

    def test_create_amenity_success(self):
        resp = self.client.post("/api/v1/amenities/", json={"name": "Pool"})
        # Check for 308/301 redirect (common slash issue)
        if resp.status_code in (301, 302, 307, 308):
            self.fail(f"Got redirect {resp.status_code}. Check trailing slash on route.")

        self.assertEqual(
            resp.status_code, 201,
            msg=f"Expected 201, got {resp.status_code}. Body: {resp.get_data(as_text=True)}"
        )
        data = resp.get_json()
        self.assertIn("id", data)
        self.assertEqual(data["name"], "Pool")

    def test_create_amenity_failure(self):
        resp = self.client.post("/api/v1/amenities/", json={"name": ""})
        if resp.status_code in (301, 302, 307, 308):
            self.fail(f"Got redirect {resp.status_code}. Check trailing slash on route.")

        self.assertEqual(
            resp.status_code, 400,
            msg=f"Expected 400, got {resp.status_code}. Body: {resp.get_data(as_text=True)}"
        )
        data = resp.get_json()
        self.assertIn("error", data)

if __name__ == "__main__":
    unittest.main()
