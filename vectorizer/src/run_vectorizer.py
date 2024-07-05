import logging, json, time
from src._drivers import OpenaiPineconeDriver
from src.inserter import Inserter
from src.feature import ProductFeature
from src.config import EMPTY_QUEUE_SLEEP_TIME
from utils import get_env_vars
from utils.rabbit import RabbitChannel, NoMessagesFoundException
from utils.product import Product

logger = logging.getLogger("src")

def insert_product_to_vdb(product: Product):
    logger.debug("Starting to insert product features to vector db.")

    metadata = {"name": product.name, "uid": product.uid}
    driver = OpenaiPineconeDriver()

    with Inserter(driver) as inserter:
        for vectorspace, text in product.features.items():
            inserter.register_feature(ProductFeature(text=text, namespace=vectorspace, metadata=metadata, driver=driver))

def send_features_to_rabbit(rabbit_client: RabbitChannel, product: Product):
    logger.debug("Starting to send product features back to backend.")

    exchange, = get_env_vars(["RABBIT_OUTPUT_EXCHANGE"],
                            required=True)
    
    metadata = {"name": product.name, "uid": product.uid}
    driver = OpenaiPineconeDriver()

    features_vectors = dict()
    for vectorspace, text in product.features.items():
        feature = ProductFeature(text=text, namespace=vectorspace, metadata=metadata, driver=driver).vector
        feature["values"] = feature["values"].tolist()
        features_vectors[vectorspace] = feature
    features_vectors_json = json.dumps(features_vectors)
    rabbit_client.publish("", product.routing_info.target_queue, features_vectors_json, correlation_id=product.routing_info.corr_id)

def main():
    rabbit_input_queue, = get_env_vars(["RABBIT_INPUT_QUEUE"], required=True)
    rabbit_channel = RabbitChannel.get_default_channel()

    while True:
        logger.info(f"Looking for message in queue '{rabbit_input_queue}'")

        try:
            _, msg = rabbit_channel.consume(rabbit_input_queue)
        except NoMessagesFoundException:
            logger.info(f"Queue empty, waiting {EMPTY_QUEUE_SLEEP_TIME} secs and trying again")
            time.sleep(EMPTY_QUEUE_SLEEP_TIME)
            continue

        product = Product.from_json(msg)
        logger.info(f"Got product {repr(product)}")

        if product.routing_info.backend_request:
            send_features_to_rabbit(rabbit_channel, product)
        else:
            insert_product_to_vdb(product)
    
if __name__ == "__main__":
    main()