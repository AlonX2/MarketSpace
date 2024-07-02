import hashlib, logging
from functools import cached_property

from src._drivers import IVectorspaceDriver, DriverError

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
       logger.debug(f"Generating embedding for feature id {feature_id} of type {self.namespace}.")

       try:
         vector = self._driver.create_vector(self.text, feature_id, self.metadata)
         logger.debug(f"Generated embedding for feature id {feature_id}.")
         return vector
       except DriverError:
         logger.error("Failed to generate embedding.")
         raise
    
    def __repr__(self) -> str:
       return f"<ProductFeature text={repr(self.text)}, namespace={repr(self.namespace)}, metadata={repr(self.metadata)}, driver={repr(self._driver)}>"
        
        