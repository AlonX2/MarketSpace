import dataclasses, json, logging

from src.clients.gpt import GPTClient
from src.resolvers import resolve_product_features, resolve_company_products
from utils import get_env_vars
from utils.product import Product, ProductRoutingInfo
from utils.rabbit import RabbitClient

logger = logging.getLogger(__package__)

class Resolver():
    """
    A class that resolves the features of the products given to it
    """
    def __init__(self, from_backend, rabbit_client: RabbitClient, output_exchange, output_routing_key) -> None:
        self.from_backend = from_backend
        self.rabbit_client = rabbit_client
        self.output_exchange = output_exchange
        self.output_routing_key = output_routing_key
        logger.info(f"Initialized Resolver with from_backend={self.from_backend}")

    def build_product_from_msg(self, props, msg):
        """
        Builds a Product instance from a given message.

        :param props: The properties of the RabbitMQ message.
        :param msg: The message content in JSON format.
        :return: An instance of the Product class.
        """
        logger.debug(f"Building product from message: props={props}, msg={msg}")
        routing_info = ProductRoutingInfo(backend_request=self.from_backend, corr_id=props.correlation_id, target_queue=props.reply_to)
        product_info = json.loads(msg)
        product = Product(uid=product_info["uid"], name=product_info["name"], url=product_info["url"], routing_info=routing_info)
        return product
    
    def send_to_vectorizer(self, product, props):
        """
        Sends the product information to a vectorizer via RabbitMQ.

        :param product: An instance of the Product class.
        :param props: The properties of the message.
        """
        logger.debug(f"Sending product to vectorizer: product={product}, props={props}")
        product_json = json.dumps(dataclasses.asdict(product))
        self.rabbit_client.publish(self.output_exchange,
                                   self.output_routing_key,
                                   product_json,
                                   correlation_id=props.correlation_id,
                                   reply_to=props.reply_to)
        logger.info(f"Product sent to vectorizer: {product_json}")

    def resolve_from_message(self, ch, method_frame, props, msg):
        """
        Resolves product information from a received message and processes it.
        """
        logger.info(f"Received message: props={props}, msg={msg}")
        gpt_client = GPTClient()
        if self.from_backend:
            products = [self.build_product_from_msg(props, msg)]
        else:
            company_url = json.loads(msg)["url"]
            logger.debug(f"Resolving company products for URL: {company_url}")
            products = resolve_company_products(gpt_client, company_url)

        for product in products:
            logger.debug(f"Resolving features for product: {product}")
            resolve_product_features(gpt_client, product)
            self.send_to_vectorizer(product, props)


def main():
    backend_input_queue, collector_input_queue, output_exchange, output_rk = get_env_vars(["RABBIT_BACKEND_INPUT_QUEUE",
                                                                                            "RABBIT_COLLECTOR_INPUT_QUEUE",
                                                                                            "RABBIT_OUTPUT_EXCHANGE",
                                                                                            "RABBIT_OUTPUT_ROUTING_KEY"],
                                                                                            required=True)
    
    logging.info("Starting to listen for messages!")
    rabbit_client = RabbitClient.get_default_client()

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
    
if __name__ == "__main__":
    main()