import pika
from utils import get_env_vars

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

        self.connection_params = pika.ConnectionParameters(**kwargs)
        
    def publish(self, exchange, routing_key, content, **kwargs):
        props = pika.BasicProperties(**kwargs) if len(kwargs) > 0 else None
            
        with pika.BlockingConnection(self.connection_params) as conn:
            channel = conn.channel()
            channel.confirm_delivery()
            channel.basic_publish(exchange=exchange,
                                routing_key=routing_key,
                                body=content,
                                properties=props)    

    def consume(self, queue):
        with pika.BlockingConnection(self.connection_params) as conn:
            channel = conn.channel()
            channel.queue_declare(queue=queue)
            get_ok, props, msg = channel.basic_get(queue=queue, auto_ack=True)
            if get_ok is None:
                raise NoMessagesFoundException("No messages in queue")
            return props, msg  