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
                                properties=props,
                                mandatory=True)    

    def consume(self, queue):
        with pika.BlockingConnection(self.connection_params) as conn:
            channel = conn.channel()
            channel.queue_declare(queue=queue)
            get_ok, props, msg = channel.basic_get(queue=queue, auto_ack=True)
            if get_ok is None:
                raise NoMessagesFoundException("No messages in queue")
            return props, msg  
        
    def async_consume(self, queue, callback):
        with pika.BlockingConnection(self.connection_params) as conn:
            channel = conn.channel()
            channel.queue_declare(queue=queue)
            channel.basic_consume(queue=queue,
                                  on_message_callback=callback,
                                  auto_ack=True)
        
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