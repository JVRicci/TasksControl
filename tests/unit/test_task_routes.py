import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.core.server import app
from src.db.base import Base
from src.models.task_model import Task
from src.models.user_model import User


@pytest.mark.parametrize(
    ("task_data", "user_data"),
    [
        (
            Task(
                title="Test Task",
                description="Description of a task",
                completed=False,
                user_id=1,
            ),
            User(name="John Doe", email="test@gmail.com", password="testpassword"),
        )
    ],
)
class TestTaskRoute:
    def test_create_a_task(self, task_data, user_data):
        # Arrange
        client = app.test_client()

        # Act
        response = client.post("/v1/tasks")

        # Assert
        assert response.status_code == 201

    def test_get_a_task(self, task_data, user_data):
        client = app.test_client()

        response = client.get("/v1/tasks")

        assert response.status_code == 200

    def test_delete_a_task(self, task_data, user_data):
        client = app.test_client()

        response = client.delete("/v1/tasks")

        assert response.status_code == 204

    def test_patching_a_task(self, task_data, user_data):
        client = app.test_client()

        response = client.patch("/v1/tasks")

        assert response.status_code == 200
