from vectorspace_inserter import VectorspaceInserter, OpenaiPineconeDriver
from product.product import Product

import logging
logging.log
prod = Product("uuid", "prod-name", "google.com", {"purpose": "To help people find content"})
VectorspaceInserter(driver=OpenaiPineconeDriver()).insert_products([prod])
