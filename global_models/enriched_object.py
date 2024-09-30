import json
import dataclasses

from global_models.object_routing_info import ObjectRoutingInfo


@dataclasses.dataclass
class EnrichedObject:
    uid: str
    name: str
    url: str
    routing_info: ObjectRoutingInfo = dataclasses.field(
        default_factory=ObjectRoutingInfo)
    features: dict[str, str] = dataclasses.field(default_factory=dict)

    @classmethod
    def from_json(cls, json_data: str):
        args = json.loads(json_data)
        routing_info = ObjectRoutingInfo(**args["routing_info"])
        return cls(uid=args["uid"], name=args["name"], url=args["url"], features=args["features"], routing_info=routing_info)
