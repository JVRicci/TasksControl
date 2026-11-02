from flask import Flask

from src.routes.health_check import api_bp

app = Flask(__name__)

app.register_blueprint(api_bp, url_prefix="/health")

if __name__ == "__main__":
    app.run(debug=True)
