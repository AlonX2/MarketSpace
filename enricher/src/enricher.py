import logging

from utils.llm_clients.interface import ILLMClient
from global_models import ResolvedObject, EnrichedObject

logger = logging.getLogger(__package__)


class Enricher():
    def __init__(self,
                 llm_client: ILLMClient,
                 enrichment_templates: dict[str, str]) -> None:
        self.llm_client = llm_client
        self.enrichment_templates = enrichment_templates

    def enrich_resolved_object(self, resolved_object: ResolvedObject) -> EnrichedObject:
        object_features = dict()
        for feature_name, feature_template in self.enrichment_templates.items():
            feature_prompt = feature_template.format(
                name=resolved_object.name, url=resolved_object.url)
            object_features[feature_name] = self.llm_client.get_response(
                feature_prompt)

        return EnrichedObject(uid=resolved_object.uid,
                              name=resolved_object.name,
                              url=resolved_object.url,
                              routing_info=resolved_object.routing_info,
                              features=object_features)
