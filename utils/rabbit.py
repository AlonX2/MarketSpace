import logging

import pika, pika.channel, pika.exceptions

from utils import get_env_vars

logger = logging.getLogger()
class RabbitChannelException(Exception):
    pass

class NoMessagesFoundException(RabbitChannelException):
    pass

class RabbitChannel():
    def __init__(self, username = None, password = None, **kwargs):
        if username or password:
            if not (username and password):
                raise RabbitChannelException("Failed to initialize rabbit client: "
                                        "Cannot provide username or password without the other (must provide both or nothing at all).")
            
            kwargs["credentials"] = pika.PlainCredentials(username, password)

        try:
            connection_params = pika.ConnectionParameters(**kwargs)
            self._connection = pika.BlockingConnection(connection_params)
            logger.info("Established connection to RabbitMQ server")
        except pika.exceptions.AMQPConnectionError as e:
            logger.error("Failed to connect to RabbitMQ server")
            raise RabbitChannelException("Failed to connect to RabbitMQ server") from e

        self._channel = self._connection.channel()
        self._channel.confirm_delivery()
        logger.info("Created channel to RabbitMQ exchange server")
     
    @classmethod
    def get_default_channel(cls, **extra_args):
        """
        Builds a default RabbitClient by the standard environment variables.
        """
        rabbit_username, rabbit_password, rabbit_host, rabbit_port = get_env_vars(["RABBIT_USERNAME",
                                                                                    "RABBIT_PASSWORD",
                                                                                    "RABBIT_HOST",
                                                                                    "RABBIT_PORT"],
                                                                                    required=True)
        
        return cls(username=rabbit_username, password=rabbit_password, host=rabbit_host, port=rabbit_port, **extra_args)
    
    def publish(self, exchange, routing_key, content, **kwargs):
        if self._connection.is_closed:
            raise RabbitChannelException("Connection to Rabbit is closed, cannot publish")
        props = pika.BasicProperties(**kwargs) if len(kwargs) > 0 else None
        
        self._channel.basic_publish(exchange=exchange,
                                routing_key=routing_key,
                                body=content,
                                properties=props,
                                mandatory=True)    

    def create_exclusive_queue(self):
        return self._channel.queue_declare(queue="", exclusive=True).method.queue

    def consume(self, queue):
        if self._connection.is_closed:
            raise RabbitChannelException("Connection to Rabbit is closed, cannot consume")
        self._channel.queue_declare(queue=queue)
        get_ok, props, msg = self._channel.basic_get(queue=queue, auto_ack=True)
        if get_ok is None:
            raise NoMessagesFoundException("No messages in queue")
        return props, msg
        
    def async_consume(self, queue, callback) -> None | str:
        if self._connection.is_closed:
            raise RabbitChannelException("Connection to Rabbit is closed, cannot async consume")
        self._channel.queue_declare(queue=queue)
        self._channel.basic_consume(queue=queue,
                                on_message_callback=callback,
                                auto_ack=True)
        
    def close(self):
        if self._connection is not None:
            self._connection.close()
        else:
            raise RabbitChannelException("Attempted to close an already closed channel")
    
    def __enter__(self):
        return self
    
    def __exit__(self, **_):
        self.close()

    def __del__(self):
        if not self._connection.is_closed:
            self.close()