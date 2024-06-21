import logging

import pika, pika.channel, pika.exceptions

from utils import get_env_vars

logger = logging.getLogger()
class RabbitClientException(Exception):
    pass

class NoMessagesFoundException(RabbitClientException):
    pass

class RabbitClient():
    def __init__(self, username = None, password = None, **kwargs):
        if username or password:
            if not (username and password):
                raise RabbitClientException("Failed to initialize rabbit client: "
                                        "Cannot provide username or password without the other (must provide both or nothing at all).")
            
            kwargs["credentials"] = pika.PlainCredentials(username, password)

        try:
            connection_params = pika.ConnectionParameters(**kwargs)
            self.connection = pika.BlockingConnection(connection_params)
            logger.info("Established connection to RabbitMQ server")
        except pika.exceptions.AMQPConnectionError as e:
            logger.error("Failed to connect to RabbitMQ server")
            raise RabbitClientException("Failed to connect to RabbitMQ server") from e

        self.channel = self.connection.channel()
        self.channel.confirm_delivery()
        logger.info("Created channel to RabbitMQ exchange server")

    def close_connection(self):
        connection: pika.channel.Channel | None = getattr(self, "connection", None)
        if connection is not None:
            connection.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, **_):
        self.close_connection()

    def __del__(self):
        self.close_connection()

    def publish(self, exchange, routing_key, content, **kwargs):
        if self.connection.is_closed():
            raise RabbitClientException("Connection to Rabbit is closed, cannot publish")
        props = pika.BasicProperties(**kwargs) if len(kwargs) > 0 else None
        
        self.channel.basic_publish(exchange=exchange,
                                routing_key=routing_key,
                                body=content,
                                properties=props,
                                mandatory=True)    

    def consume(self, queue):
        if self.connection.is_closed():
            raise RabbitClientException("Connection to Rabbit is closed, cannot consume")
        result = self.channel.queue_declare(queue=queue)
        get_ok, props, msg = self.channel.basic_get(queue=queue, auto_ack=True)
        if get_ok is None:
            raise NoMessagesFoundException("No messages in queue")
        return props, msg, result.method.queue if queue == "" else None
        
    def async_consume(self, queue, callback) -> None | str:
        if self.connection.is_closed():
            raise RabbitClientException("Connection to Rabbit is closed, cannot async consume")
        result = self.channel.queue_declare(queue=queue)
        self.channel.basic_consume(queue=queue,
                                on_message_callback=callback,
                                auto_ack=True)
        if queue == "":
            return result.method.queue
        
    @classmethod
    def get_default_client(cls, **extra_args):
        """
        Builds a default RabbitClient by the standard environment variables.
        """
        rabbit_username, rabbit_password, rabbit_host, rabbit_port = get_env_vars(["RABBIT_USERNAME",
                                                                                    "RABBIT_PASSWORD",
                                                                                    "RABBIT_HOST",
                                                                                    "RABBIT_PORT"],
                                                                                    required=True)
        
        return cls(username=rabbit_username, password=rabbit_password, host=rabbit_host, port=rabbit_port, **extra_args)