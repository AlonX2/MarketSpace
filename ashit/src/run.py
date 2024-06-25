import logging

from src.app import create_app, socketio

logger = logging.getLogger(__package__)
logger.warning("SHITssssssssssssssssssssssssssssssssssssssssssssssssssss")
app = create_app()

socketio.run(app)