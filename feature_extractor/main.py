from __future__ import annotations
from product.product import Product
from feature_extractor.prompt_generator import IPromptGenerator
from feature_extractor.llm_client import ILLMClient

class FeatureResolver:
    def __init__(self, prompt_generator: IPromptGenerator, llm_client: ILLMClient) -> None:
        self._prompt_generator = prompt_generator
        self._llm_client = llm_client

    def resolve_features(self, products: list[Product]) -> dict[str, str]:
        for product in products:
            feature_prompts = self._prompt_generator.get_prompts(product)
            for feature_name, prompt in feature_prompts.items():
                product.features[feature_name] = self._llm_client.get_response(prompt)
        return products


def main():
    pass


if __name__ == "__main__":
    main()