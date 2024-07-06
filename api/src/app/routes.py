import logging, json

import pydantic
from flask import Blueprint, Response, request

from src.app.handlers import get_similar_products, GetSimilarProductsException
from src.app.validation_models.product_description import ProductDescription

logger = logging.getLogger(__package__)

products_bp = Blueprint("products", __name__)

# @products_bp.get("/products")
# def handle_get_similar_products():
#     res = {"problem": {"namespace": "problem", "matches": [{"id": "ee0f2262bc9f571e7c7f50c05b6c888e34681283cd034796c101dd3626aa5216", "score": 0.79970026, "values": [], "sparse_values": {"indices": [], "values": []}, "metadata": {"uid": "61699bc4-8722-473d-ba73-7fc06228ad60", "name": "Accessibility Audits"}}, {"id": "450792ff2bacb123ba689818365f8f36c7a4f65836e2427d1687761f49931deb", "score": 0.76085556, "values": [], "sparse_values": {"indices": [], "values": []}, "metadata": {"uid": "181e829c-716e-402b-b66b-8332e5635998", "name": "Accessibility Consulting"}}, {"id": "ea605fd2d1af50bfbd0c5062f0929bbdea6445a463f698b8ba3d8cdc8da1179e", "score": 0.7153777, "values": [], "sparse_values": {"indices": [], "values": []}, "metadata": {"uid": "d68ded83-9975-4012-a2f8-f159201110a1", "name": "ADA Compliance Website Services"}}, {"id": "4b8d264e4b9d14ec5fb0b8bcf7254aa6ce2a2d2b4cebfa7c15516266505bc264", "score": 0.69974184, "values": [], "sparse_values": {"indices": [], "values": []}, "metadata": {"uid": "2b755b07-af24-483d-b830-1748dc64c338", "name": "ADA WebGuard"}}, {"id": "ad568a47535c3b5d2906d19e11f8d64e67be5aef340152f5e673ab445a3aff4a", "score": 0.69794655, "values": [], "sparse_values": {"indices": [], "values": []}, "metadata": {"uid": "c557c62c-837e-4452-9758-bca3bec09252", "name": "ADA Compliance Software"}}], "usage": {"read_units": 6}}, "market": {"namespace": "market", "matches": [{"id": "8f840f5db5feb972206735ccb9a6e6e30dd53ef00769ba51ad31b07fd29b4e50", "score": 0.8662775, "values": [], "sparse_values": {"indices": [], "values": []}, "metadata": {"uid": "61699bc4-8722-473d-ba73-7fc06228ad60", "name": "Accessibility Audits"}}, {"id": "3b2dc86e7558298abf920c454d713badfa90d5b9a34d605261220a24068d3205", "score": 0.8188166, "values": [], "sparse_values": {"indices": [], "values": []}, "metadata": {"uid": "f12fb565-86f8-41e2-a62f-19c6d6bbf16c", "name": "Consultancy"}}, {"id": "c84cb73968708c45231f894b433fd83f930bc75a11abca367b502e7fb85cea88", "score": 0.8182805, "values": [], "sparse_values": {"indices": [], "values": []}, "metadata": {"uid": "181e829c-716e-402b-b66b-8332e5635998", "name": "Accessibility Consulting"}}, {"id": "0bc8a90d72d5a29bb086d76c1f7dce7c708876dea4c7c936db78d451ad38bc9d", "score": 0.7885502, "values": [], "sparse_values": {"indices": [], "values": []}, "metadata": {"uid": "7e2ff9e1-02f0-4fce-ba73-31cfe9011fd2", "name": "Document Accessibility"}}, {"id": "6ba10ccdf1a4a197a18a4c677b3f915d1436efa9a318c168be55848bd8feba04", "score": 0.7734097, "values": [], "sparse_values": {"indices": [], "values": []}, "metadata": {"uid": "f68067f3-543d-4415-a0da-facd8823d200", "name": "Accessibility Training"}}], "usage": {"read_units": 6}}}
#     return json.dumps(res)
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