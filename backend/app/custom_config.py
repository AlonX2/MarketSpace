from db_client import IDbClient, PineconeClient
from app.microservice_client import MicroserviceClient

class CustomConfig():
    def __init__(self) -> None:
        self.db_client: IDbClient = PineconeClient()
        self.microservice_client = MicroserviceClient()