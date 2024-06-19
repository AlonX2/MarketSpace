import pika, pika.exceptions, uuid, logging

from typing import Callable

from utils.call_future import CallFuture
from ._config import *
from .exceptions import *

logger = logging.getLogger(__package__)

class MicroserviceClient():
    """A singleton for making RPC call to the different microservices the backend is a client of
    """
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(MicroserviceClient, cls).__new__(cls)
        return cls.instance
    
    def __init__(self) -> None:
        """Initializes the `MicroserviceClient` class.

        Initializes the connection and the callback queue of the client.

        :raises MicroserviceClientFailedRabbitConnection: Raised in case of failure to connect to RabbitMQ server.
        """
        self._call_record: dict[uuid.UUID, CallFuture] = {}
        try:
            connection_params = pika.ConnectionParameters(RABBITMQ_SERVER)
            self._connection = pika.BlockingConnection(connection_params)
            logger.info("Established connection to RabbitMQ server")
        except pika.exceptions.AMQPConnectionError as e:
            logger.error("Failed to connect to RabbitMQ server")
            raise MicroserviceClientFailedRabbitConnection("Failed to connect to RabbitMQ server") from e
        
        self._channel = self._connection.channel()
        logger.info("Created channel to RabbitMQ exchange server")

        self._res_queue = self._create_exclusive_queue(message_callback=self._on_res)

        logger.info("Instance created")
    
    def __del__(self):
        """Closes the connection to RabbitMQ server upon object destruction
        """
        connection = getattr(self, "_connection", None)
        if connection is not None:
            connection.close()

    def _create_exclusive_queue(self, message_callback: Callable) -> str:
        """Creates exclusive queue for this client

        :param message_callback: The callback to be called upon getting messages from the newly created queue.
        :return: The created queue name
        """
        result = self._channel.queue_declare(queue='', exclusive=True)
        _queue_name = result.method.queue

        logger.info(f"Callback queue created: {_queue_name}")

        self._channel.basic_consume(
            queue=_queue_name,
            on_message_callback=message_callback,
            auto_ack=True)
        return _queue_name

    def _on_res(self, ch, method, props, body) -> None:
        """The callback function that handles responses from the different microservices, 
        and returns them to the original caller, resuming the caller context. 
        The parameters it gets are default for RabbitMQ queue callback.

        :param ch: The channel object.
        :param method: Delivery information.
        :param props: AMQP properties.
        :param body: Message body.
        """
        if props.correlation_id in self._call_record:
            call_future = self._call_record[props.correlation_id]

            if "error" in props.headers and props.headers["error"] == "true":
                call_future.set_error(MicroserviceFailed(body))
                del self._call_record[props.correlation_id]
                return
            call_future.set_result(body)
            del self._call_record[props.correlation_id]
            return
        logger.warning("MicroserviceClient got an unexpected correlation id in it\'s callback queue")

    def invoke(self, target_queue: str, data_json: str) -> str:
        """Sends a RPC request to the target according to the parameter `target_queue`

        :param product_desc: The product description to be sent
        :param res_callback: The callback to send the response to
        :return: A list of similar products returned by the service

        :raises MicroserviceClientException: Raised if RabbitMQ errros, `target_queue` doesn't exist
        or nacked by the exchange.
        """

        corr_id = str(uuid.uuid4())
        _call_future = CallFuture()
        self._call_record[corr_id] = _call_future
        
        try:
            self._channel.basic_publish(
                exchange="",
                routing_key=target_queue,
                properties=pika.BasicProperties(
                    reply_to=self._res_queue,
                    correlation_id=corr_id,
                ),
                body=data_json)
        except (pika.exceptions.NackError, pika.exceptions.UnroutableError) as e:
            logger.error("Couldn\'t publish a message to RabbitMQ exchange")
            raise MicroserviceClientException("RabbitMQ error") from e
        
        _call_future.happened.wait()
        if _call_future.error is not None:
            logger.error(str(_call_future.error))
            raise _call_future.error
        
        logger.info("Succesfult acquired result from the microservice")
        return _call_future.result