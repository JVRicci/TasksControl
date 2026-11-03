from flask import Flask

from src.routes.health_check import api_bp
from src.routes.v1.router import api_bp as task_bp

app = Flask(__name__)

app.register_blueprint(api_bp, url_prefix="/health")
app.register_blueprint(task_bp, url_prefix="/v1")
