import pytest

from src.core.server import app

from src.models.user_model import User


@pytest.mark.parametrize(
    ("user_data"),
    [User(name="John Doe", email="test@gmail.com", password="testpassword")],
)
class TestUsersRoutes:
    def test_a_user_creation(self, user_data):
        # arrange
        client = app.test_client()

        # act
        response = client.post(
            "/v1/users",
            json={
                "name": user_data.name,
                "email": user_data.email,
                "password": user_data.password,
            },
        )

        # assert
        assert response.status_code == 201

    def test_get_user(self, user_data):
        # arrange
        client = app.test_client()

        # act
        created_user = client.post(
            "/v1/users",
            json={
                "name": user_data.name,
                "email": "test_user2@gmail.com",
                "password": user_data.password,
            },
        )

        assert created_user.status_code == 201

        user_id = created_user.get_json()["id"]
        response = client.get(
            f"/v1/users/{user_id}",
        )

        # assert
        assert response.status_code == 200
