import logging
import logging

from utils import get_env_vars
from utils.rabbit import RabbitClient
from src.resolver import Resolver

logger = logging.getLogger("src")


def main():
    backend_input_queue, collector_input_queue, output_exchange, output_rk = get_env_vars(["RABBIT_BACKEND_INPUT_QUEUE",
                                                                                            "RABBIT_COLLECTOR_INPUT_QUEUE",
                                                                                            "RABBIT_OUTPUT_EXCHANGE",
                                                                                            "RABBIT_OUTPUT_ROUTING_KEY"],
                                                                                            required=True)
    
    logging.info("Starting to listen for messages!")
    rabbit_client = RabbitChannel.get_default_channel()
    with open("nigger2.txt", "w") as f:
        f.write("fuck")
    backend_resolver = Resolver(from_backend=True,
                                rabbit_client=rabbit_client,
                                output_exchange=output_exchange,
                                output_routing_key=output_rk)
    
    collection_resolver = Resolver(from_backend=False,
                                   rabbit_client=rabbit_client,
                                   output_exchange=output_exchange,
                                   output_routing_key=output_rk)  
      
    rabbit_client.async_consume(backend_input_queue, backend_resolver.resolve_from_message)
    rabbit_client.async_consume(collector_input_queue, collection_resolver.resolve_from_message)
    logger.info("RabbitMQ consumers initialized and listening.")
    
    rabbit_client.start_consuming()
    
if __name__ == "__main__":
    main()