import requests
from src.exceptions import CrunchbaseQueryError
from utils import get_env_vars

PAGINATION_BATCH_SIZE = 500
class CrunchbaseSearchQuery():
    def __init__(self, url, requested_fields):
        if len(requested_fields) == 0:
            raise CrunchbaseQueryError(f"Query must have at least 1 requested field. Got the following fields list: {requested_fields}")
        
        self._url = url
        self._query = {"field_ids": requested_fields}

    def execute(self):
        api_key, = get_env_vars(["CRUNCHBASE_API_KEY"], required=True)
        entities = []

        self._ensure_query_integrity()

        executing_query = self._query.copy()

        while True:
            executing_query["limit"] = PAGINATION_BATCH_SIZE

            if len(entities) > 0:
                previous_item_id = entities[-1]["uuid"]
                executing_query["after_id"] = previous_item_id

            resp = requests.post(self._url, params={"user_key": api_key}, json=executing_query)
            if not resp.status_code == 200:
                raise CrunchbaseQueryError(f"Failed to perform query, got status code {resp.status_code}")
            
            content = resp.json()
            entities.extend(content["entities"])

            if len(content["entities"]) < PAGINATION_BATCH_SIZE:
                break

        return entities

    def add_filter(self, field_name, operator, filter_value):
        if "query" not in self._query:
            self._query["query"] = []

        filter_value = filter_value if isinstance(filter_value, list) else [filter_value]

        filter = {
            "type": "predicate",
            "field_id": field_name,
            "operator_id": operator,
            "values": filter_value     
        }
        self._query["query"].append(filter)

    def define_sorting(self, key_field, desc=True):
        if "order" in self._query:
            raise CrunchbaseQueryError(f"Attempted to define query sorting when it already exists. Current query state: {self._query}")
        
        self._query["order"] = {
                     "field_id": key_field,
                     "sort": "desc" if desc else "asc"
                 }

    def _ensure_query_integrity(self):
         if "query" not in self._query:
            raise CrunchbaseQueryError(f"Query must have at least 1 filter. Current query state: {self._query}")



