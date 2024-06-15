import hashlib, logging
from pika import PlainCredentials
from functools import cached_property

from vectorizer._drivers import IVectorspaceDriver, DriverError
from vectorizer.feature import ProductFeature
from utils.product import Product
from utils import get_env_vars
from utils.rabbit import RabbitClient

logger = logging.getLogger(__package__)

class ProductFeature():
    def __init__(self, text: str, namespace: str, metadata: dict, driver: IVectorspaceDriver):
        self.text = text
        self.namespace = namespace
        self.metadata = metadata

        self._driver = driver

    @cached_property
    def vector(self):
       feature_id = hashlib.sha256(self.text.encode()).hexdigest() 

       try:
         vector = self._driver.create_vector(self.text, feature_id, self.metadata)
         logger.debug(f"Generated embedding for feature id {feature_id} of type {self.namespace}")
         return vector
       except DriverError:
         logger.error("Failed to generate embedding.")
         raise
        
        