from .clients.interface import ILLMClient

class PromptTemplateRunner():
    """
    A class used to run prompts with a given template using an LLM client.
    """
    def __init__(self, llm_client: ILLMClient, template: str) -> None:
        self._template = template
        self._llm_client = llm_client

    def run(self, **kwargs):
        """
        Generates a prompt by formatting the template with the given keyword arguments and 
        retrieves a response from the LLM client.

        :param kwargs: Arbitrary keyword arguments to format the template.
        :return: The response from the LLM client.
        """
        prompt = self._template.format(**kwargs)
        return self._llm_client.get_response(prompt)
    