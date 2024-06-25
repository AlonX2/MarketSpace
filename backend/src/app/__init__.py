from flask import Flask 

from src.app.custom_config import CustomConfig
from src.app.events import socketio

def create_app():
    app = Flask(__name__)
    app.config["DEBUG"] = True

    app.config["CUSTOM"] = CustomConfig()
    socketio.init_app(app)

    return app
