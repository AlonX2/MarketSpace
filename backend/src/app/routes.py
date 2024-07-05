import logging, json

import pydantic
from flask import Blueprint, Response, request

from src.app.handlers import get_similar_products, GetSimilarProductsException
from src.app.validation_models.product_description import ProductDescription

logger = logging.getLogger(__package__)

products_bp = Blueprint("products", __name__)

@products_bp.get("/products")
def handle_get_similar_products():
    product_url = request.args.get("url", default = "", type = str)
    product_name = request.args.get("name", default = "", type = str)
    product_desc = {"name": product_name, "url": product_url}
    try:
        ProductDescription.model_validate(product_desc)
    except pydantic.ValidationError as e:
        logger.info(f"Got invalid Product description")
        return Response(str(e), status=400)
    try:
        similar_products = get_similar_products(product_desc)
        similar_products_json = json.dumps(similar_products)
        logger.info(f"Finished processing similar_products_request.\nThe similar products json is:\n{similar_products_json}")
        return Response(similar_products_json)
    except GetSimilarProductsException as e:
        logger.info(f"Could\'nt get similar products")
        return Response(str(e), status=500)