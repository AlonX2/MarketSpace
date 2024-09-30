import json
import logging

from utils import get_env_vars
from utils.llm_clients import GPTClient
from src.enricher import Enricher
from src.enricher_rabbit_wrapper import EnricherRabbitWrapper, RabbitChannel

logger = logging.getLogger(__package__)


def read_templates(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.loads(f.read())


def main():
    input_queue, \
        output_exchange, \
        output_rk, \
        enrichment_templates_path, \
        openai_api_key = get_env_vars(["RABBIT_INPUT_QUEUE",
                                       "RABBIT_OUTPUT_EXCHANGE",
                                       "RABBIT_OUTPUT_ROUTING_KEY",
                                       "ENRICHMENT_TEMPLATES_PATH",
                                       "OPENAI_API_KEY"],
                                      required=True)
    gpt_client = GPTClient(openai_api_key)
    logger.debug("GPTClient initialized")
    enricher = Enricher(gpt_client, read_templates(enrichment_templates_path))
    logger.debug("Enricher initialized")

    rabbit_channel = RabbitChannel.get_default_channel()
    enricher_rabbit_wrapper = EnricherRabbitWrapper(
        enricher, rabbit_channel, output_rk, output_exchange)

    rabbit_channel.async_consume(
        input_queue, enricher_rabbit_wrapper.enrich_from_message)
    logger.info("RabbitMQ consumers initialized and listening.")

    rabbit_channel.start_consuming()
