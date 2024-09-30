import logging
import json
import dataclasses

from global_models import ResolvedObject, EnrichedObject
from utils.rabbit import RabbitChannel
from src.enricher import Enricher


logger = logging.getLogger(__package__)


class EnricherRabbitWrapper():
    def __init__(self, enricher: Enricher, rabbit_channel: RabbitChannel, output_routing_key: str, output_exchange: str) -> None:
        self.enricher = enricher
        self.rabbit_channel = rabbit_channel
        self.output_routing_key = output_routing_key
        self.output_exchange = output_exchange

    def enrich_from_message(self, ch, method_frame, props, msg):
        """
        Enriches resolved object information from a received message and processes it.
        """
        logger.info(f"Received message: props={props}, msg={msg}")
        resolved_object = self.build_resolved_object_from_msg(props, msg)

        logger.debug(f"Resolving features for ResolvedObject: {
                     resolved_object}")
        enriched_object = self.enricher.enrich_resolved_object(resolved_object)
        self.send_to_vectorizer(enriched_object, props)

    def build_resolved_object_from_msg(self, props, msg):
        """
        Builds a ResolvedObject instance from a given message.

        :param props: The properties of the RabbitMQ message.
        :param msg: The message content in JSON format.
        :return: An instance of the ResolvedObject class.
        """
        logger.debug(
            f"Building resolved_object from message: props={props}, msg={msg}")
        resolved_object = ResolvedObject.from_json(msg)
        return resolved_object

    def send_to_vectorizer(self, enriched_object: EnrichedObject, props):
        """
        Sends the EnrichedObject to a vectorizer via RabbitMQ.

        :param enriched_object: An instance of the EnrichedObject class.
        :param props: The properties of the message.
        """
        logger.debug(
            f"Sending enriched_object to vectorizer: enriched_object={enriched_object}, props={props}")

        enriched_object_json = json.dumps(dataclasses.asdict(enriched_object))
        self.rabbit_channel.publish(self.output_exchange,
                                    self.output_routing_key,
                                    enriched_object_json,
                                    correlation_id=props.correlation_id,
                                    reply_to=props.reply_to)
        logger.info(f"EnrichedObject sent to vectorizer: {
                    enriched_object_json}")
