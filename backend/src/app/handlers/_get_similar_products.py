import json, logging, pinecone

from flask import current_app

from src.app.microservice_client import MicroserviceClient, MicroserviceClientException

logger = logging.getLogger(__package__)

FEATURE_RESOLVER_QUEUE = "feature_resolver_queue"
EMBEDDER_QUEUE = "embedder_queue"
DB_SEARCHER_QUEUE = "db_searcher_queue"

class GetSimilarProductsException(Exception):
    """Generic exception for the get_similar_products handler
    """
    pass

def get_similar_products(product_desc_json: str | bytes) -> dict[str, list[str]]:
    """Retrieve similar products based on the given product description JSON.
    Uses `MicroserviceClient` with the configured microservices queues, and the vector db client
    in order to retreive the similar products already in the vector DB.

    :param product_desc_json: JSON string or bytes containing the product description.
    :return: A dictionary where keys are features and values are lists of similar products by this feature.
    :raises GetSimilarProductsException: If there is an issue with feature resolvance and embedding
                                         or querying the database for similar products.
    """
    try:
        microservice_client: MicroserviceClient = current_app.config["CUSTOM"].microservice_client
        vdb_index: pinecone.Index = current_app.config["CUSTOM"].vdb_index
    except KeyError:
        logger.error("Couldn\'t access microservice_client and/or vdb_index from CUSTOM config of app")
        raise
    
    try:        
        product_embeddings_json: str = microservice_client.invoke(target_queue=FEATURE_RESOLVER_QUEUE, data_json=product_desc_json)
    except MicroserviceClientException as e:
        logger.error("Feature resolvance and embedding failed")
        raise GetSimilarProductsException("Feature resolvance and embedding failed") from e
    
    product_embeddings: dict[str, list] = json.loads(product_embeddings_json)
    logger.info("Got product embeddings from FeatureResolver/Embedder")

    similar_products: dict[str, list[str]] = dict()
    for feature_name, embedding in product_embeddings.items():
        similar_products[feature_name] = vdb_index.query(vector=embedding, namespace=feature_name, top_k=5)
    
    logger.info("Finished acquiring similar products")
    return similar_products