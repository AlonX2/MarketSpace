from abc import ABC, abstractmethod

class ILLMClient(ABC):
    """An interface for a generic LLM client.
    """
    @abstractmethod
    def get_response(self, prompt: str) -> str:
        """Gets the response of the LLM according to a prompt given to it.

        :param prompt: The prompt for the LLM
        """
        raise NotImplementedError()