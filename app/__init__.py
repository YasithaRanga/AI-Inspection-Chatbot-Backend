from flask import Flask
from .routes.query import query_bp
from flask_cors import CORS


def create_app():
    app = Flask(__name__)

    CORS(app)
    
    app.register_blueprint(query_bp, url_prefix="/api")

    return app
