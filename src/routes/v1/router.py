from flask import Blueprint

from src.routes.v1.tasks import Task

api_bp = Blueprint("v1", __name__)

api_bp.add_url_rule("/tasks", view_func=Task.as_view("task"))
