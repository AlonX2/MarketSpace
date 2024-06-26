import logging

from utils import get_env_vars
from utils.rabbit import RabbitChannel
from src.resolver import Resolver
from src.clients import GPTClient

logger = logging.getLogger("src")


def main():
    backend_input_queue, collector_input_queue, output_exchange, output_rk, openai_api_key = get_env_vars(["RABBIT_BACKEND_INPUT_QUEUE",
                                                                                            "RABBIT_COLLECTOR_INPUT_QUEUE",
                                                                                            "RABBIT_OUTPUT_EXCHANGE",
                                                                                            "RABBIT_OUTPUT_ROUTING_KEY",
                                                                                            "OPENAI_API_KEY"],
                                                                                            required=True)
    
    gpt_client = GPTClient(api_key=openai_api_key)
    logging.info("Starting to listen for messages!")
    rabbit_channel = RabbitChannel.get_default_channel()
    backend_resolver = Resolver(from_backend=True,
                                rabbit_channel=rabbit_channel,
                                llm_client=gpt_client,
                                output_exchange=output_exchange,
                                output_routing_key=output_rk)
    
    collection_resolver = Resolver(from_backend=False,
                                   rabbit_channel=rabbit_channel,
                                   llm_client=gpt_client,
                                   output_exchange=output_exchange,
                                   output_routing_key=output_rk)  
      
    rabbit_channel.async_consume(backend_input_queue, backend_resolver.resolve_from_message)
    rabbit_channel.async_consume(collector_input_queue, collection_resolver.resolve_from_message)
    logger.info("RabbitMQ consumers initialized and listening.")
    
    rabbit_channel.start_consuming()
    
if __name__ == "__main__":
    main()