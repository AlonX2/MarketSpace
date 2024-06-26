import logging

logger = logging.getLogger(__package__)

from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO()
@socketio.on("connect")
def handle_connect():
    logger.warning("User connected")
    print("shit")

def create_app():
    app = Flask(__name__)
    print(logger)
    print(__package__)

    return app