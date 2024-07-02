import logging

import pydantic
from flask import request
from flask_socketio import emit

from src.app.extensions import socketio
from src.app.handlers import get_similar_products, GetSimilarProductsException
from src.app.validation_models.product_description import ProductDescription

logger = logging.getLogger(__package__)

@socketio.on("connect")
def handle_connect():
    """
    Handle a user connection event.
    """
    logger.info(f"User connected with session id: {request.sid}")

@socketio.on("similar_products_request")
def handle_get_similar_products(product_desc: dict):
    """Handle a request for similar products.

    Validates the product description JSON, emits an error message if validation fails, 
    and attempts to retrieve similar products. Emits the results or an error message 
    based on the outcome of the retrieval process.

    :param product_desc_json: JSON string or bytes containing the product description.
    """
    logger.info("similar_products_request event called")
    try:
        ProductDescription.model_validate(product_desc)
    except pydantic.ValidationError as e:
        emit("similar_products_error", str(e))
        logger.error(f"Parameter product_desc_json isn\'t valid: {str(e)}")
        return
    try:
        logger.error("BITCHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
        products_json = get_similar_products(product_desc)
        emit("similar_products_response", products_json)
        logger.info("Finished processing similar_products_request")
    except GetSimilarProductsException as e:
        emit("similar_products_error", str(e))
        logger.info(f"Could\'nt get similar products")