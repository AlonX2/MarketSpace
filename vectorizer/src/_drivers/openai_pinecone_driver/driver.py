import logging, numpy as np

from pinecone import Pinecone
from openai import OpenAI

from src._drivers import IVectorspaceDriver, DriverError
from ._config import BATCH_SIZE
from utils import get_env_vars
from utils.logging import format_logged_substring

logger = logging.getLogger(__package__)

class OpenaiPineconeDriver(IVectorspaceDriver):
    RECOMMENDED_BATCH_SIZE = BATCH_SIZE
    def __init__(self):
        openai_key, pinecone_key, pinecone_index = get_env_vars(["OPENAI_API_KEY",
                                                                 "PINECONE_API_KEY",
                                                                 "PINECONE_INDEX_NAME"], required=True)
        try:
            self.openai_client = OpenAI(api_key=openai_key)
            self.pinecone_index = Pinecone(api_key=pinecone_key).Index(pinecone_index)
        except Exception as e:
            raise DriverError("Failed to initialize openai and pinecone clients, possibly because of bad API keys.") from e

    def _get_embedding(self, text: str, model: str ="text-embedding-3-small") -> np.ndarray:
        """
        Creates a vector embedding from text using an openai embedding model.
        :param text: The text to create the embedding from.
        :param model: The openai model identifier for the model to create the embedding with.
        :returns: A numpy array for the generated vector embedding.
        """

        logger.debug(f"Generating embedding for text: {format_logged_substring(text)}, with model {format_logged_substring(model)}")

        try:
            embedding = self.openai_client.embeddings.create(input=[text], model=model).data[0].embedding
        except Exception as e:
            raise DriverError(f"Failed to generate embedding for text: '{text}', model:'{model}'.") from e


        logger.debug(f"Embedding for text: '{text[:30]}...' generated!")

        return np.array(embedding)
    
    
    def insert(self, vectors: list , vectorspace: str):
        logger.debug(f"Inserting {len(vectors)} vectors into namespace '{vectorspace}'...")
        try:
            self.pinecone_index.upsert(vectors=vectors, namespace=vectorspace)
        except Exception as e:
            raise DriverError(f"Failed to upsert vectors: {vectors} into namespace '{vectorspace}'") from e
        
        logger.debug(f"Inserted {len(vectors)} vectors into namespace '{vectorspace}'!")


    def create_vector(self, text: str, id: str, metadata: dict = None) -> dict:
        vector = {"id": id, "values": self._get_embedding(text)}
        if metadata is not None:
            vector["metadata"] = metadata
        return vector
