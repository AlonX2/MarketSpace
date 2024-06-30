from flask import Flask

from utils.logging import setup_logger
from src.app.custom_config import CustomConfig
from src.app.events import socketio

def _setup_logger():
    """
    Setups logging for the vectorspace_driver package.
    """

    import logging
    logger = logging.getLogger(__package__)
    logger.name = "backend"
    setup_logger(logger)

_setup_logger()

def create_app():
    app = Flask(__name__)
    app.config["DEBUG"] = True
    app.config["CUSTOM"] = CustomConfig()
    socketio.init_app(app, cors_allowed_origins="*")

    return app