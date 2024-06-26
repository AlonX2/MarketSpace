import logging

from src.app import create_app, socketio

logger = logging.getLogger(__package__)
logger.info("Starting flask server")
app = create_app()

socketio.init_app(app)
logger.info("Started flask server")