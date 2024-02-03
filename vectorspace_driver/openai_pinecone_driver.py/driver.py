from pinecone import Pinecone
from openai import OpenAI
import numpy as np

PINECONE_API_KEY = "e4d3c997-d68d-4f03-a42a-6c60c6dd9b02"
OPENAI_API_KEY = "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"
PINECONE_INDEX_NAME = "test"
RES_FILE = "out.txt"

class OpenaiPineconeDriver():
    def __init__(self):
        self.openai_client = OpenAI(api_key=OPENAI_API_KEY)
        self.pinecone_index = Pinecone(api_key=PINECONE_API_KEY).Index(PINECONE_INDEX_NAME)

    def _get_embedding(self, text, model="text-embedding-3-small"):
        return np.array(
            self.openai_client.embeddings.create(input=[text], model=model).data[0].embedding
        )
    
    def insert(self, vectors, vectorspace):
        self.pinecone_index.upsert(vectors=vectors, namespace=vectorspace)

    def preprocess_vector(self, text, id, metadata=None):
        vector = {"id": id, "values": self._get_embedding(text)}
        if metadata is not None:
            vector["metadata"] = metadata
        return vector
