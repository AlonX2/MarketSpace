import sys

sys.path.extend(["../.", "../../.", "../../../.", "../../."])

import pytest
from unittest.mock import MagicMock, patch
from flask import Flask
from flask_socketio.test_client import SocketIOTestClient

from src.app import socketio

@pytest.fixture
def socketio_client_fixture():
    app = Flask(__name__)
    socketio.init_app(app)
    socketio_client = socketio.test_client(app)

    with app.app_context():
        socketio_client.connect()
        yield socketio_client
        socketio_client.disconnect()

def test_connection(socketio_client_fixture: SocketIOTestClient):
    pass