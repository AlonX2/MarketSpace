import sys, pytest, json
sys.path.extend([".", "../."])

from flask import Flask
from flask_socketio.test_client import SocketIOTestClient
from unittest.mock import patch, MagicMock

from src.app.events import socketio
from src.app.events import GetSimilarProductsException

@pytest.fixture
def socketio_client_fixture():
    app = Flask(__name__)
    socketio.init_app(app)
    socketio_client = socketio.test_client(app)

    with app.app_context():
        socketio_client.connect()
        yield socketio_client
        socketio_client.disconnect()

@pytest.fixture
def pass_validation():
    with patch("app.events.ProductDescription.model_validate_json", return_value=None) as validate_mock:
        yield
        validate_mock.assert_called_once()

@pytest.mark.parametrize("product_desc_json",
                         [
                             "",
                             "a",
                             json.dumps({"a": 3}),
                         ])
def test_invalidProductDescJson_similarProductsRequest_returnError(socketio_client_fixture: SocketIOTestClient, product_desc_json: str):
    socketio_client_fixture.emit(
        "similar_products_request",
        product_desc_json
    )
    responses = socketio_client_fixture.get_received()
    assert len(responses) == 1
    response = responses[0]

    assert response["name"] == "similar_products_error"
    assert "validation error" in response["args"][0]

def test_serviceUnavailale_similarProductsRequest_returnError(socketio_client_fixture: SocketIOTestClient, pass_validation):
    with patch("backend.app.events.get_similar_products", side_effect=GetSimilarProductsException("test_error_message")) as get_similar_products_mock:
        socketio_client_fixture.emit(
            "similar_products_request",
            "test_input"
        )
    responses = socketio_client_fixture.get_received()
    assert len(responses) == 1
    response = responses[0]
    assert response["name"] == "similar_products_error"
    assert response["args"][0] == "test_error_message"

    get_similar_products_mock.assert_called_once_with("test_input")

def test_normalCall_similarProductsRequest_returnResults(socketio_client_fixture: SocketIOTestClient, pass_validation):
    with patch("backend.app.events.get_similar_products", return_value="similar_products_test") as get_similar_products_mock:
        socketio_client_fixture.emit(
            "similar_products_request",
            "test_input"
        )
    responses = socketio_client_fixture.get_received()
    assert len(responses) == 1
    response = responses[0]
    assert response["name"] == "similar_products_response"
    assert response["args"][0] == "similar_products_test"

    get_similar_products_mock.assert_called_once_with("test_input")