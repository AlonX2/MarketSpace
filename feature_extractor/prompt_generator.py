from __future__ import annotations
from abc import ABC, abstractmethod
from product.product import Product


class IPromptGenerator(ABC):
    @abstractmethod
    def get_prompts(self, product: Product) -> dict[str, str]:
        raise NotImplementedError()

    def __repr__(self) -> str:
        # TODO: implement the representation of this object so it could be evaluated and statisticd
        raise NotImplementedError()
    
class PromptGeneratorA:
    def __init__(self) -> None:
        self._prompts_template = {
            "Purpose": "Go to \"{product.url}\", and write a very short sentence about their primary purpose. DO NOT INCLUDE ANY BUZZWORDS AND BE SPACIFIC ABOUT THE VALUE AND TECHNICAL DETAILS OF THE PRODUCT!"
        }

    def get_prompts(self, product: Product) -> dict[str, str]:
        return {k: t.format(product=product) for k, t in self._prompts_template.items()}