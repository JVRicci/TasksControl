from flask import Blueprint

from src.routes.v1.tasks_controller import TaskController
from src.routes.v1.user_controller import UserController

api_bp = Blueprint("v1", __name__)

api_bp.add_url_rule("/tasks", view_func=TaskController.as_view("task"))

user_view = UserController.as_view("user")
api_bp.add_url_rule("/users", view_func=user_view, methods=["POST"])
api_bp.add_url_rule(
    "/users/<int:user_id>",
    view_func=user_view,
    methods=["GET"],
)
