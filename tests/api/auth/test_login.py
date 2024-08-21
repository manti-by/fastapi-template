from app.users.models import User
from fastapi.testclient import TestClient

from tests import DEFAULT_PASSWORD


class TestLogin:
    def setup_method(self):
        self.url = "/api/v1/auth/token/"
        self.headers = {"Content-Type": "application/x-www-form-urlencoded"}

    def test_login(self, client: TestClient, user: User):
        response = client.post(
            self.url,
            data={"username": user.email, "password": DEFAULT_PASSWORD},
            headers=self.headers,
        )
        assert response.status_code == 200

    def test_login__invalid_payload(self, client: TestClient):
        response = client.post(self.url, data={}, headers=self.headers)
        assert response.status_code == 422

    def test_login__invalid_method(self, client: TestClient):
        response = client.get(self.url)
        assert response.status_code == 405
