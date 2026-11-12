import logging
from pathlib import Path

from flasgger import Swagger
from flask import Flask

from src.db.base import Base
from src.db.database import engine
from src.models.idempotency_model import IdempotencyRecord
from src.routes.health_check import api_bp as health_bp
from src.routes.v1.router import api_bp as api_v1_bp

# Cria a base de dados caso não existir
Base.metadata.create_all(bind=engine)

app = Flask(__name__)

swagger_file = Path(__file__).resolve().parents[2] / "swagger.yml"

Swagger(
    app,
    template_file=str(swagger_file),
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

app.register_blueprint(health_bp, url_prefix="/health")
app.register_blueprint(api_v1_bp, url_prefix="/v1")
