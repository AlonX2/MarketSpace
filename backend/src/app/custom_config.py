from pinecone.grpc import PineconeGRPC as Pinecone

from utils.env import get_env_vars
from src.app.microservice_client import MicroserviceClient

class CustomConfig():
    def __init__(self) -> None:
        pinecone_apikey, pc_index_name = get_env_vars(["PINECONE_API_KEY", "PINECONE_INDEX_NAME"], required=True)
        pc = Pinecone(api_key=pinecone_apikey)
        self.vdb_index = pc.Index(pc_index_name)
        self.microservice_client = MicroserviceClient()