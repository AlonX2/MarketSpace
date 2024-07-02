from pinecone.grpc import PineconeGRPC as Pinecone

from utils.rabbit import RabbitChannel
from src.app.microservice_client import MicroserviceClient

from unittest.mock import MagicMock
class CustomConfig():
    def __init__(self) -> None:
        #TODO: change it, maybe from env vars
        # pc = Pinecone(api_key="YOUR_API_KEY")
        # self.vdb_index = pc.Index("example-index")
        self.vdb_index = MagicMock()
        self.microservice_client = MicroserviceClient(RabbitChannel.get_default_channel())