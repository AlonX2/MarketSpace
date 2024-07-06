from flask import Flask

from utils.logging import setup_logger
from src.app.custom_config import CustomConfig
from src.app.routes import products_bp

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
    @app.get("/")
    def shit():
        return "DAMN"

    app.register_blueprint(products_bp)
    return app