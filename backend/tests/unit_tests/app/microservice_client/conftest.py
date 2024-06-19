import sys, pytest
sys.path.extend([".", "../."])

from unittest.mock import patch, MagicMock

from src.app.microservice_client.microservice_client import MicroserviceClient

@pytest.fixture
def microservice_client_fixture():
    with patch.object(MicroserviceClient, '__init__', lambda _: None):
        microservice_client_fixture = MicroserviceClient()
        microservice_client_fixture._channel = MagicMock()
        microservice_client_fixture._call_record = dict()
        yield microservice_client_fixture