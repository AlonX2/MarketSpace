import json
from dataclasses import dataclass, field

@dataclass
class ProductRoutingInfo():
    backend_request: bool
    corr_id: int = None
    target_queue: str = None


@dataclass
class Product:
    uid: str
    name: str
    url: str
    routing_info: ProductRoutingInfo
    features: dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_json(cls, json_data: str):
        args = json.loads(json_data)
        routing_info = ProductRoutingInfo(**args["routing_info"])
        return cls(uid=args["uid"], name=args["name"], url=args["url"], features=args["features"], routing_info=routing_info)
