import random
import string

import pytest
from uuid import uuid4
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.core.server import app
from src.db.base import Base
from src.models.task_model import Task
from src.models.user_model import User


def random_char(char_num):
    return "".join(random.choice(string.ascii_letters) for _ in range(char_num))


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
            User(name=uuid4(), email=f"{random_char(7)}@gmail.com", password=uuid4()),
        )
    ],
)
class TestTaskRoute:
    def test_create_a_task(self, task_data, user_data):
        # Arrange
        client = app.test_client()

        # Act
        user_response = client.post(
            "/v1/users",
            json={
                "name": user_data.name,
                "email": user_data.email,
                "password": user_data.password,
            },
        )

        assert user_response.status_code == 201

        user_id = user_response.json["id"]

        response = client.post(
            "/v1/tasks",
            json={
                "title": task_data.title,
                "description": task_data.description,
                "completed": task_data.completed,
                "user_id": user_id,
            },
        )

        # Assert
        assert response.status_code == 201

    def test_get_tasks(self, task_data, user_data):
        client = app.test_client()

        user_response = client.post(
            "/v1/users",
            json={
                "name": user_data.name,
                "email": f"{random_char(7)}@gmail.com",
                "password": user_data.password,
            },
        )
        assert user_response.status_code == 201

        user_id = user_response.json["id"]
        task_response = client.post(
            "/v1/tasks",
            json={
                "title": task_data.title,
                "description": task_data.description,
                "completed": task_data.completed,
                "user_id": user_id,
            },
        )
        assert task_response.status_code == 201

        response = client.get(f"/v1/tasks?user_id={user_id}")

        assert response.status_code == 200
        assert any(task["id"] == task_response.json["id"] for task in response.json)

    def test_patching_a_task(self, task_data, user_data):
        client = app.test_client()

        user_response = client.post(
            "/v1/users",
            json={
                "name": user_data.name,
                "email": f"{random_char(7)}@gmail.com",
                "password": user_data.password,
            },
        )
        assert user_response.status_code == 201

        user_id = user_response.json["id"]
        task_response = client.post(
            "/v1/tasks",
            json={
                "title": task_data.title,
                "description": task_data.description,
                "completed": task_data.completed,
                "user_id": user_id,
            },
        )
        assert task_response.status_code == 201

        updated_response = client.patch(
            f"/v1/tasks?user_id={user_id}",
            json={
                "id": task_response.json["id"],
                "title": task_data.title,
                "description": task_data.description,
                "completed": task_data.completed,
                "user_id": user_id,
            },
        )

        assert updated_response.status_code == 202
        # assert any(task["id"] == task_response.json["id"] for task in response.json)

    def test_delete_a_task(self, task_data, user_data):
        client = app.test_client()

        response = client.delete("/v1/tasks")

        assert response.status_code == 204
