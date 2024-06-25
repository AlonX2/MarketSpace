import logging, json

from openai import OpenAI

from ..interface import ILLMClient

logger = logging.getLogger(__package__)

class GPTClient(ILLMClient):
    """GPT client, implementation of the ILLMClient interface.
    """
    def __init__(self, api_key: str) -> None:
        try:
            self._client = OpenAI(api_key=api_key)
        except:
            logger.error("Could not instansiate new OpenAI client, check OPENAI_API_KEY")
            raise
    
    def get_response(self, prompt) -> str:
        """Gets the response from the GPT instance for the prompt given to it.

        :param prompt: Prompt for the GPT instance.
        :return: The response from the GPT instance.
        """
        try:
            res = self._client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                response_format={ "type": "json_object" },
                messages=[
                        {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                        {"role": "user", "content": prompt}
                    ]
                ).choices[0].message.content
            return res
        except:
            logger.error("Could not get response from GPT client.")
            raise