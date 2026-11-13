from flask import Blueprint

from src.routes.v1.auth_controller import auth_bp, AuthController
from src.routes.v1.tasks_controller import api_bp as tasks_bp
from src.routes.v1.user_controller import api_bp as users_bp

api_bp = Blueprint("v1", __name__)

auth_bp.add_url_rule(
    "/login",
    view_func=AuthController.as_view("login"),
    methods=["POST"],
)

api_bp.register_blueprint(auth_bp)
api_bp.register_blueprint(tasks_bp)
api_bp.register_blueprint(users_bp)
