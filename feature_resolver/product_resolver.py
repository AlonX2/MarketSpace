import logging

from .clients import ILLMClient 

logger =  logging.getLogger(__package__)

class ProductResolver():
    def __init__(self, llm_client: ILLMClient, prompt_template: str) -> None:
        self._llm_client = llm_client
        self._prompt_template = prompt_template

    def resolve_products(self, company: dict[str, str]):
        prompt = self._prompt_template.format(url=company["url"])
        return self._llm_client.get_response(prompt)