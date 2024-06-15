import pytest, threading, pytest, pika, pika.exceptions

from unittest.mock import patch, MagicMock

from app.microservice_client.exceptions import MicroserviceClientException, MicroserviceFailed
from app.microservice_client.microservice_client import MicroserviceClient


@pytest.fixture
def invoke_microservice_client_fixture(microservice_client_fixture: MicroserviceClient):
    microservice_client_fixture._res_queue = "res_queue_test"

    call_future = MagicMock()
    basic_publish_mock = MagicMock()
    microservice_client_fixture._channel.basic_publish = basic_publish_mock
    basic_publish_mock.side_effect = lambda _: None

    with (patch("uuid.uuid4", return_value="test_uuid"),
          patch("utils.call_future.CallFuture", return_value=call_future)):
        yield microservice_client_fixture

def assert_basic_publish_args(basic_publish_mock: MagicMock):
    basic_publish_mock.assert_called_once()
    call_args = basic_publish_mock.call_args
    assert call_args[1]['exchange'] == ""
    assert call_args[1]['routing_key'] == "target_queue_test"
    assert call_args[1]['body'] == "data_json_test"
    assert call_args[1]['properties'].reply_to == "res_queue_test"
    assert call_args[1]['properties'].correlation_id == "test_uuid"


def test_succesfulInvocation_invoke_returnRes(invoke_microservice_client_fixture: MicroserviceClient):
    def basic_publish_side_effect(*_, **__):
        def got_message():
            call_future = invoke_microservice_client_fixture._call_record["test_uuid"]
            call_future.set_result("test_result")
            
        t = threading.Thread(target=got_message)
        t.start()
    invoke_microservice_client_fixture._channel.basic_publish.side_effect = basic_publish_side_effect

    assert invoke_microservice_client_fixture.invoke("target_queue_test", data_json="data_json_test") == "test_result"
    assert_basic_publish_args(invoke_microservice_client_fixture._channel.basic_publish)

def test_microserviceFailed_invoke_returnFutureWithError(invoke_microservice_client_fixture: MicroserviceClient):
    def basic_publish_side_effect(*_, **__):
        def got_message():
            call_future = invoke_microservice_client_fixture._call_record["test_uuid"]
            call_future.set_error(MicroserviceFailed("test_error"))
            
        t = threading.Thread(target=got_message)
        t.start()
    invoke_microservice_client_fixture._channel.basic_publish.side_effect = basic_publish_side_effect

    with pytest.raises(MicroserviceFailed, match="test_error"):
        invoke_microservice_client_fixture.invoke("target_queue_test", data_json="data_json_test")
    assert_basic_publish_args(invoke_microservice_client_fixture._channel.basic_publish)

def test_nonExistentQueue_invoke_raiseMicroserviceClientException(invoke_microservice_client_fixture: MicroserviceClient):
    def basic_publish_side_effect(*_, **__):
        raise pika.exceptions.UnroutableError("")
    invoke_microservice_client_fixture._channel.basic_publish.side_effect = basic_publish_side_effect
    
    with pytest.raises(MicroserviceClientException, match="RabbitMQ error"):
        invoke_microservice_client_fixture.invoke("target_queue_test", "data_json_test")
    assert_basic_publish_args(invoke_microservice_client_fixture._channel.basic_publish)