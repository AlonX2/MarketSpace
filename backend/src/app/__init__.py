from flask import Flask 

from src.app.custom_config import CustomConfig
from src.app.events import socketio

def create_app():
    app = Flask(__name__)
    app.config["DEBUG"] = True

    app.config["CUSTOM"] = CustomConfig()
    socketio.init_app(app)

    return app

def _setup_logger():
    """
    Setups logging for the backend.
    """
    
    import logging
    logger = logging.getLogger(__package__)
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s - %(name)s - %(levelname)s]:  %(message)s')

    ch.setFormatter(formatter)

    logger.addHandler(ch)

_setup_logger()