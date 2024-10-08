from fastapi.testclient import TestClient


class TestHealthcheck:
    def setup_method(self):
        self.url = "/api/v1/health/"

    def test_health(self, client: TestClient):
        response = client.get(self.url)
        assert response.status_code == 200

    def test_health__invalid_method(self, client: TestClient):
        response = client.post(self.url, follow_redirects=True)
        assert response.status_code == 405
