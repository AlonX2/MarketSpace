from .clients.interface import ILLMClient

class PromptTemplateRunner():
    def __init__(self, llm_client: ILLMClient, template: str) -> None:
        self._template = template
        self._llm_client = llm_client

    def run(self, **kwargs):
        prompt = self._template.format(**kwargs)
        return self._llm_client.get_response(prompt)
    