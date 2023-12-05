from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from .routes import auth, algo
from . import config

def create_app():
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = config.JWT_SECRET

    CORS(app)
    JWTManager(app)

    @app.route("/", methods=("GET",))
    def index():
        return "Schedule Backend"
    
    app.register_blueprint(auth)
    app.register_blueprint(algo)

    return app
