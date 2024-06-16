import logging, json, time

from src._drivers import OpenaiPineconeDriver
from src.inserter import Inserter
from src.feature import ProductFeature
from src.config import EMPTY_QUEUE_SLEEP_TIME
from utils import get_env_vars
from utils.rabbit import RabbitClient, NoMessagesFoundException
from utils.product import Product

logger =  logging.getLogger(__package__)

def insert_product_to_vdb(product: Product):
    logger.debug("Starting to insert product features to vector db.")

    metadata = {"name": product.name, "uid": product.uid}
    driver = OpenaiPineconeDriver()

    with Inserter() as inserter:
        for vectorspace, text in product.features.items():
            inserter.register_feature(ProductFeature(text=text, vectorspace=vectorspace, metadata=metadata, driver=driver))

def send_features_to_rabbit(rabbit_client: RabbitClient, product: Product):
    logger.debug("Starting to send product features back to backend.")

    exchange = get_env_vars(["RABBIT_OUTPUT_EXCHANGE"],
                            required=True)
    
    metadata = {"name": product.name, "uid": product.uid}
    driver = OpenaiPineconeDriver()

    for vectorspace, text in product.features.items():
        feature = ProductFeature(text=text, vectorspace=vectorspace, metadata=metadata, driver=driver).vector
        feature_json = json.dumps(feature)
        rabbit_client.publish(exchange, product.routing_info.target_queue, feature_json, correlation_id=product.routing_info.corr_id)

def main():
    rabbit_input_queue = get_env_vars(["RABBIT_INPUT_QUEUE"], required=True)
    rabbit_client = RabbitClient.get_default_client()

    while True:
        logger.info(f"looking for message in queue {rabbit_input_queue}...")

        try:
            _, msg = rabbit_client.consume(rabbit_input_queue)
        except NoMessagesFoundException:
            logger.info(f"Queue empty, waiting {EMPTY_QUEUE_SLEEP_TIME} secs and trying again...")
            time.sleep(EMPTY_QUEUE_SLEEP_TIME)
            continue

        product = Product.from_json(msg)
        logger.info(f"Got product {repr(product)}")

        if product.routing_info.backend_request:
            send_features_to_rabbit(rabbit_client, product)
        else:
            insert_product_to_vdb(product)

if __name__ == "__main__":
    main()