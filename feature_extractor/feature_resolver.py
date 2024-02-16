from product.product import Product
from .clients.interface import ILLMClient

class FeatureResolver:
    def __init__(self, llm_client: ILLMClient, feature_prompt_templates: dict[str, str]) -> None:
        """Constructer function for FeatureResolver class.

        :param llm_client: The LLM client used for anlayzing the product.
        :param feature_prompt_templates: Templates, each rendered to a 
        prompt, specific for each product. The prompts are then used to query 
        the LLM client for the feature of this product.
        The key of each template should be the name of the feature.
        The template itself should be injectable by `Product` instances.
        """
        
        self._llm_client = llm_client
        self._feature_prompt_templates = feature_prompt_templates

    def _render_templates(self, product: Product) -> dict[str, str]:
        """Renders the prompt templates to valid prompts on the given product.

        :param product: The product to render the template according to.
        :return: List of prompts specific to the product.
        """
        feature_prompts = {}
        for name, template in self._feature_prompt_templates.items():
            feature_prompts[name] = template.format(product=product)
        return feature_prompts
    
    def _resolve_product_features(self, product: Product) -> Product:
        """Resolves the features of a singular product according to the LLM
        client used.

        :param product: The product that needs feature resolutions.
        :return: The product after feature resolutions.
        """
        feature_prompts = self._render_templates(product)
        for name, prompt in feature_prompts.items():
            product.features[name] = self._llm_client.get_response(prompt)
        return product
    
    def resolve_features(self, products: list[Product]) -> list[Product]:
        """Resolves the features of all products given to it. 

        :param products: The products that need feature resolutions.
        :return: The products after feature resolutions.
        """
        return [self._resolve_product_features(product) for product in products]