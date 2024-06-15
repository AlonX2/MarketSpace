import pytest, uuid

from unittest.mock import patch, MagicMock
from typing import Tuple

from backend.app.microservice_client import MicroserviceClient


@pytest.fixture
def on_res_microservice_client_fixture(microservice_client_fixture: MicroserviceClient):
    corr_id = str(uuid.uuid4())
    call_future = MagicMock()
    
    props_mock = MagicMock()
    props_mock.correlation_id = corr_id
    props_mock.headers = dict()
    microservice_client_fixture._call_record = {corr_id: call_future}
    
    return microservice_client_fixture, props_mock, corr_id, call_future

def test_microserviceInvocationFailed_onRes_setCallFutureException(on_res_microservice_client_fixture: Tuple[MicroserviceClient, MagicMock, str, MagicMock]):
    microservice_client_fixture, props_mock, corr_id, call_future = on_res_microservice_client_fixture
    props_mock.headers["error"] = "true"

    with patch("app.microservice_client.microservice_client.MicroserviceFailed") as MicroserviceFailed_mock:
        MicroserviceFailed_mock.return_value = "MicroserviceFailed_test"
        microservice_client_fixture._on_res(None, None, props_mock, "test_error")

        MicroserviceFailed_mock.assert_called_once_with("test_error")
        call_future.set_error.assert_called_once_with("MicroserviceFailed_test")
        assert corr_id not in microservice_client_fixture._call_record

def test_gotResult_onRes_setCallFutureException(on_res_microservice_client_fixture: Tuple[MicroserviceClient, MagicMock, str, MagicMock]):
    microservice_client_fixture, props_mock, corr_id, call_future = on_res_microservice_client_fixture

    microservice_client_fixture._on_res(None, None, props_mock, "test_result")

    call_future.set_result.assert_called_once_with("test_result")
    assert corr_id not in microservice_client_fixture._call_record