import logging

logger = logging.getLogger(__package__)

from flask import Flask
from flask_socketio import SocketIO


socketio = SocketIO()
@socketio.on("connect")
def handle_connect():
    logger.warning("DMANNNNNNN")
    print("shit")

def create_app():
    app = Flask(__name__)
    print(logger)
    print(__package__)
    logger.warning("IIIIIIIIIIIIIIIIIIIIIIIIIIIIII")    
    return app