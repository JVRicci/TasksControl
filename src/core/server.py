import logging

from flask import Flask

from src.db.base import Base
from src.db.database import engine
from src.routes.health_check import api_bp as health_bp
from src.routes.v1.router import api_bp as api_v1_bp

# This will create a new database if she doens't exists
Base.metadata.create_all(bind=engine)

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

app.register_blueprint(health_bp, url_prefix="/health")
app.register_blueprint(api_v1_bp, url_prefix="/v1")
