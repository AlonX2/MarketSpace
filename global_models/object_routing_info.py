import dataclasses


@dataclasses.dataclass
class ObjectRoutingInfo():
    backend_request: bool = False
    corr_id: int = None
    target_queue: str = None
