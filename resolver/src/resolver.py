import dataclasses, json, logging, uuid

from utils.product import Product, ProductRoutingInfo
from utils.rabbit import RabbitChannel
from src.clients.interface import ILLMClient
from src._templates import *

logger = logging.getLogger(__package__)


class Resolver():
    """
    A class that resolves the features of the products given to it
    """

    def __init__(self, from_backend, rabbit_channel: RabbitChannel, llm_client: ILLMClient, output_exchange, output_routing_key) -> None:
        self.from_backend = from_backend
        self.rabbit_channel = rabbit_channel
        self.llm_client = llm_client
        self.output_exchange = output_exchange
        self.output_routing_key = output_routing_key
        logger.info(
            f"Initialized Resolver with from_backend={self.from_backend}")

    def build_product_from_msg(self, props, msg):
        """
        Builds a Product instance from a given message.

        :param props: The properties of the RabbitMQ message.
        :param msg: The message content in JSON format.
        :return: An instance of the Product class.
        """
        logger.debug(
            f"Building product from message: props={props}, msg={msg}")
        routing_info = ProductRoutingInfo(
            backend_request=self.from_backend, corr_id=props.correlation_id, target_queue=props.reply_to)
        product_info = json.loads(msg)
        product = Product(uid=product_info["uid"], name=product_info["name"],
                          url=product_info["url"], routing_info=routing_info)
        return product

    def send_to_vectorizer(self, product, props):
        """
        Sends the product information to a vectorizer via RabbitMQ.

        :param product: An instance of the Product class.
        :param props: The properties of the message.
        """
        logger.debug(
            f"Sending product to vectorizer: product={product}, props={props}")
        product_json = json.dumps(dataclasses.asdict(product))
        self.rabbit_channel.publish(self.output_exchange,
                                    self.output_routing_key,
                                    product_json,
                                    correlation_id=props.correlation_id,
                                    reply_to=props.reply_to)
        logger.info(f"Product sent to vectorizer: {product_json}")

    def load_templates_from_file(self):
        pass

    def resolve_from_template(self, template: str, **kwargs):
        prompt = template.format(**kwargs)
        res = self.llm_client.get_response(prompt)
        return json.loads(res)

    def resolve_company_products(self, company_url: str):
        """
        Resolves the products of a given company using the LLM client.
        """
        products_desc_list = self.resolve_from_template(
            COMPANY_PRODUCTS_PROMPT, company_url=company_url)["output"]
        logger.warning(products_desc_list)
        return [Product(str(uuid.uuid4()), name=product["product_name"], url=product["product_url"]) for product in products_desc_list]

    def resolve_product_features(self, product_name: str, product_url: str):
        """
        Resolves the features of a given product using the LLM client.
        """
        product_features = dict()
        for feature_name, feature_template in FEATURES_PROMPTS.items():
            product_features[feature_name] = self.resolve_from_template(
                feature_template, product_name=product_name, product_url=product_url)
        return product_features

    def resolve_from_message(self, ch, method_frame, props, msg):
        """
        Resolves product information from a received message and processes it.
        """
        logger.info(f"Received message: props={props}, msg={msg}")
        if self.from_backend:
            products = [self.build_product_from_msg(props, msg)]
        else:
            company_url = json.loads(msg)["url"]
            logger.debug(f"Resolving company products for URL: {company_url}")
            products = self.resolve_company_products(company_url)

        for product in products:
            logger.debug(f"Resolving features for product: {product}")
            product.features = self.resolve_product_features(
                product.name, product.url)
            self.send_to_vectorizer(product, props)
