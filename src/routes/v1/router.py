from flask import Blueprint

from src.routes.v1.auth_controller import auth_bp
from src.routes.v1.tasks_controller import api_bp as tasks_bp
from src.routes.v1.user_controller import api_bp as users_bp

api_bp = Blueprint("v1", __name__)

api_bp.register_blueprint(auth_bp)
api_bp.register_blueprint(tasks_bp)
api_bp.register_blueprint(users_bp)
