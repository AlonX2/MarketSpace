import logging, json, uuid

from utils.product import Product
from .clients.interface import ILLMClient
from ._templates import *

logger = logging.getLogger(__package__)

def resolve_product_features(llm_client: ILLMClient, product: Product):
    logger.info(f"Resolving features for product: {product}")
    for feature_name, prompt_template in FEATURES_PROMPTS.items():
        feature_prompt = prompt_template.format(url=product.url, name=product.name)
        logger.debug(f"Sending prompt to LLM: {feature_prompt}")
        product.features[feature_name] = llm_client.get_response(feature_prompt)
        logger.info(f"Resolved feature '{feature_name}' for product '{product.name}': {product.features[feature_name]}")

class ResolveCompanyProductsError(Exception):
    pass

def resolve_company_products(llm_client: ILLMClient, company_url: str) -> list[Product]:
    logger.info(f"Resolving products for company URL: {company_url}")
    prompt = COMPANY_PRODUCTS_PROMPT.format(company_url=company_url)
    logger.debug(f"Sending prompt to LLM: {prompt}")
    response = llm_client.get_response(prompt)

    try:
        products_dict = json.loads(response)
        logger.info(f"Received product data from LLM: {products_dict}")
    except json.JSONDecodeError as e:
        msg = f"Couldn't resolve products of company: {company_url}\nLLM client returned invalid Json."
        logger.error(msg)
        raise ResolveCompanyProductsError(msg) from e
    
    try:
        return [Product(uuid.uuid4(), name=products_dict["product_name"], url=products_dict["product_url"])]
    except KeyError as e:
        msg = f"Couldn't resolve products of company: {company_url}\nOne or more of the products returned by the LLM client doesn't have the proper structure"
        logger.error(msg)
        raise ResolveCompanyProductsError(msg) from e