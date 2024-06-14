from dataclasses import dataclass

@dataclass
class Product:
    uid: str
    name: str
    url: str
    features: dict[str, str]
    backend_request: bool
    backend_id: int = None