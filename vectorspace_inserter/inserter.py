import hashlib, logging

from vectorspace_inserter._drivers import IVectorspaceDriver, DriverError
from product.product import Product

logger =  logging.getLogger(__package__)

class VectorspaceInserter():
    """
    A class that provides functionality for inserting features of products into a vector database.
    """

    def __init__(self, driver: IVectorspaceDriver):
        self.driver = driver
        self.features: dict[str, list] = {} 
        logger.debug(f"Initialized vectorspace inserter object {repr(self)}")

    def _add_feature(self, text: str, metadata: dict[str, str|dict], feature_type: str):
        """
        Method that registers a feature to be entered into the vector database. The feature will only be inserted to the database on a _insert_features call.
        This function also performs all the preprocessing that the string needs in order to be entered to the db (such as creating an embedding). 
        :param text: The feature's content (that the embedding will be created with).
        :param metadata: Any additional metadata that will be inserted to the database with the embedding (eg. product name, product id, etc...).
        :param feature_type: A string that identifies the feature category (such as "primery purpose", "target customer" and so on).
        """

        feature_id = hashlib.sha256(text.encode()).hexdigest()

        try:
            vector = self.driver.create_vector(text, feature_id, metadata)
        except DriverError:
            logger.error("Failed to generate embedding.")
            raise

        if feature_type not in self.features:
            self.features[feature_type] = []

        self.features[feature_type].append(vector)

        logger.debug(f"Registered feature embedding with id {feature_id} and feature type '{feature_type}'.")
    
    def _add_product_features(self, product: Product):
        """
        Register all features of a specific product. This does not actually insert the features to the db, but creates the embeddings and stores them locally.
        :param product: The product to add the features of. 
        """
        for feature_type, text in product.features.items():
            metadata = {"product_name": product.name, "product_id": product.uid}
            self._add_feature(text, metadata, feature_type)
        
        logger.info(f"Registered {len(product.features)} feature embeddings for product '{product.name}' (id '{product.uid}').")
    
    def _insert_features(self):
        """
        Inserts all the locally saved features to the vector database, with a namespace that is determined by their type.
        """
        try:
            for namespace, vectors in self.features.items():
                self.driver.insert(vectors, namespace)
        except DriverError:
            logger.error("Failed to insert vectors into vector db.")
            raise

        logger.info(f"Inserted {len(self.features)} feature embeddings to the vector db.")
        self.features = {}
    
    def insert_products(self, products: list[Product]):
        """
        Inserts the features of a list of products to the vector database in chunks. 
        :param products: The products to insert the features of to the vector db.
        """
        logger.info(f"Currently inserting {len(products)} products...")

        for product in products:
            self._add_product_features(product)
            
            longest_feature_list = max(self.features.values(), key=lambda val: len(val))
            if len(longest_feature_list) > self.driver.RECOMMENDED_BATCH_SIZE:
                self._insert_features()

        self._insert_features()
        logger.info(f"Finished inserting {len(products)} products!")
