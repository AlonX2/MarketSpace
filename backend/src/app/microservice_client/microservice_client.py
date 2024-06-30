import uuid, logging

from utils.rabbit import RabbitChannel
from utils.call_future import CallFuture
from utils.env import get_env_vars
from ._config import *
from .exceptions import *

logger = logging.getLogger(__package__)
rabbit_exchange, = get_env_vars(["RABBIT_EXCHANGE"], required=True)

class MicroserviceClient():
    """A singleton for making RPC call to the different microservices the backend is a client of
    """
    def __new__(cls, rabbit_channel: RabbitChannel):
        if not hasattr(cls, 'instance'):
            cls.instance = super(MicroserviceClient, cls).__new__(cls)
        return cls.instance
    
    def __init__(self, rabbit_channel: RabbitChannel) -> None:
        """Initializes the `MicroserviceClient` class.

        Initializes the connection and the callback queue of the client.

        :raises MicroserviceClientFailedRabbitConnection: Raised in case of failure to connect to RabbitMQ server.
        """
        self._call_record: dict[uuid.UUID, CallFuture] = {}
        self._rabbit_channel = rabbit_channel
        self._res_queue = rabbit_channel.create_exclusive_queue()
        rabbit_channel.async_consume(self._res_queue, self._on_res, do_declare=False)
        logger.info("Instance created")

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

    def invoke(self, routing_key: str, data_json: str) -> str:
        """Sends a RPC request to the target according to the parameter `target_queue`

        :param product_desc: The product description to be sent
        :param res_callback: The callback to send the response to
        :return: A list of similar products returned by the service

        :raises MicroserviceClientException: Raised if RabbitMQ errros, `target_queue` doesn't exist
        or nacked by the exchange.
        """
        logger.info(f"Microservice Client invoked with routing key: \"{routing_key}\"\nAnd with data: \"{data_json}\"")
        corr_id = str(uuid.uuid4())
        _call_future = CallFuture()
        self._call_record[corr_id] = _call_future
        
        self._rabbit_channel.publish(
            exchange=rabbit_exchange,
            routing_key=routing_key,
            content=data_json,
            reply_to=self._res_queue,
            correlation_id=corr_id)
        
        _call_future.happened.wait()
        if _call_future.error is not None:
            logger.error(str(_call_future.error))
            raise _call_future.error
        
        logger.info("Succesfuly acquired result from the microservice")
        return _call_future.result