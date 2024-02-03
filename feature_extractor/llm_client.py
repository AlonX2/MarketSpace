from __future__ import annotations
from abc import ABC, abstractmethod
from openai import OpenAI
import json


OPENAI_API_KEY = "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"

class ILLMClient:
    @abstractmethod
    def get_response(self, prompt: str):
        raise NotImplementedError()
    
    
class GPTClient(ILLMClient):
    def __init__(self) -> None:
        self._client = OpenAI(api_key=OPENAI_API_KEY)
        
    
    def get_response(self, prompt):
        res = self._client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            response_format={ "type": "json_object" },
            messages=[
                    {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                    {"role": "user", "content": prompt}
                ]
            ).choices[0].message.content
        
        return json.loads(res)["message"]