from src.app.microservice_client import MicroserviceClient

def test_calling_createExclusiveQueue_returnNewQueueName(microservice_client_fixture: MicroserviceClient):
    microservice_client_fixture._channel.queue_declare.return_value.method.queue = 'test_queue'
    assert microservice_client_fixture._create_exclusive_queue("message_callback") == 'test_queue'
    
    microservice_client_fixture._channel.basic_consume.assert_called_once_with(
        queue='test_queue',
        on_message_callback="message_callback",
        auto_ack=True
    )