import unittest
from app import create_app
class TestAmenityEndpoints(unittest.TestCase):
    def setUp(self):
        # If your factory supports it, pass a testing config
        # self.app = create_app("testing")
        self.app = create_app()
        self.app.config.update(TESTING=True)
        self.client = self.app.test_client()
    def test_create_amenity_success(self):
        resp = self.client.post("/api/v1/amenities", json={"name": "Pool"})
        # If your API uses trailing slash, switch to "/api/v1/amenities/"
        # resp = self.client.post("/api/v1/amenities/", json={"name": "Pool"})
        # Catch the common “wrong slash” redirect case (308/301/302)
        if resp.status_code in (301, 302, 307, 308):
            self.fail(f"Got redirect {resp.status_code}. Check trailing slash on route. "
                      f"Location: {resp.headers.get('Location')}")
        self.assertEqual(
            resp.status_code, 201,
            msg=f"Expected 201, got {resp.status_code}. Body: {resp.get_data(as_text=True)}"
        )
    def test_create_amenity_failure(self):
        resp = self.client.post("/api/v1/amenities", json={"name": ""})
        if resp.status_code in (301, 302, 307, 308):
            self.fail(f"Got redirect {resp.status_code}. Check trailing slash on route. "
                      f"Location: {resp.headers.get('Location')}")
        self.assertEqual(
            resp.status_code, 400,
            msg=f"Expected 400, got {resp.status_code}. Body: {resp.get_data(as_text=True)}"
        )
if __name__ == "__main__":
    unittest.main()
