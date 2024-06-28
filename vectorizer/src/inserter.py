import logging

from src._drivers import IVectorspaceDriver, DriverError
from src.feature import ProductFeature

logger = logging.getLogger(__package__)

class Inserter():
    """
    A class that provides functionality for inserting features of products into a vector database.
    """

    def __init__(self, driver: IVectorspaceDriver):
        self._driver = driver
        self._features: dict[str, list] = {} 
    
    def insert_features(self):
        """
        Inserts all the locally saved features to the vector database, with a namespace that is determined by their type.
        """
        try:
            for namespace, vectors in self._features.items():
                self._driver.insert(vectors, namespace)
        except DriverError:
            logger.error("Failed to insert vectors into vector db.")
            raise

        logger.info(f"Inserted {len(self._features)} feature embeddings to the vector db.")
        self._features = {}

    def register_feature(self, feature: ProductFeature):
        logger.debug(f"registring feature '{feature}' for insertion.")
        if feature.namespace not in self._features:
            self._features[feature.namespace] = []

        self._features[feature.namespace].append(feature.vector)

        longest_feature_list = max(self._features.values(), key=len)
        if len(longest_feature_list) > self._driver.RECOMMENDED_BATCH_SIZE:
            self.insert_features()

    def __enter__(self):
        return self

    def __exit__(self, exc_type ,*_):
        if exc_type is not None:
            return
        self.insert_features()