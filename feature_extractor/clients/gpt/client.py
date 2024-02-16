import json

from openai import OpenAI
from ..interface import ILLMClient


OPENAI_API_KEY = "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"

    
class GPTClient(ILLMClient):
    """GPT client, implementation of the ILLMClient interface.
    """
    def __init__(self) -> None:
        self._client = OpenAI(api_key=OPENAI_API_KEY)
        
    
    def get_response(self, prompt):
        """Gets the response from the GPT instance for the prompt given to it.

        :param prompt: Prompt for the GPT instance.
        :return: The response from the GPT instance.
        """
        res = self._client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            response_format={ "type": "json_object" },
            messages=[
                    {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                    {"role": "user", "content": prompt}
                ]
            ).choices[0].message.content
        
        return json.loads(res)["message"]