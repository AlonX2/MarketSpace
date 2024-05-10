import requests
from src.exceptions import CrunchbaseQueryError
from utils import get_env_vars

PAGINATION_BATCH_SIZE = 500
class CrunchbaseSearchQuery():
    """
    Class for building and executing crunchbase search queries.
    """

    def __init__(self, url, requested_fields):
        if len(requested_fields) == 0:
            raise CrunchbaseQueryError(f"Query must have at least 1 requested field. Got the following fields list: {requested_fields}")
        
        self._url = url
        self._query = {"field_ids": requested_fields}

    def execute(self) -> list[dict]:
        """
        Execute the query with pagination until theres no more results.
        :returns: List of all returned entities.
        """

        api_key, = get_env_vars(["CRUNCHBASE_API_KEY"], required=True)

        self._ensure_query_integrity()

        executing_query = self._query.copy()
        executing_query["limit"] = PAGINATION_BATCH_SIZE

        entities = []
        while True:
            if len(entities) > 0:
                previous_item_id = entities[-1]["uuid"]
                executing_query["after_id"] = previous_item_id
            try:
                resp = requests.post(self._url, params={"user_key": api_key}, json=executing_query)
            except requests.exceptions.RequestException as e:
                raise CrunchbaseQueryError(f"Failed to perform query due to requests error.") from e
                
            if resp.status_code != 200:
                raise CrunchbaseQueryError(f"Failed to perform query, got status code {resp.status_code}")
            
            content = resp.json()
            entities.extend(content["entities"])

            if len(content["entities"]) < PAGINATION_BATCH_SIZE:
                break

        return entities

    def add_filter(self, field_name: str, operator: str, filter_value: str):
        """
        Adds a filter (search condition) to the query.
        :param field_name: The org info field to exert the condition on.
        :param operator: The operator between the field and the value (eg. "Includes", "lte", "gte", "Equals").
        :param filter_value: The value to check in comperison with the field_name and operator,
                             The value the field needs to have to meet the condition.
        """

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

    def define_sorting(self, key_field: str, desc: bool = True):
        """
        Defines a sorting for the query, by a specific field.
        :param key_field: The field to sort the query results by.
        :param desc: Whether the results should be sorted in a descending order (otherwise ascending).
        """

        if "order" in self._query:
            raise CrunchbaseQueryError(f"Attempted to define query sorting when it already exists. Current query state: {self._query}")
        
        self._query["order"] = {
                     "field_id": key_field,
                     "sort": "desc" if desc else "asc"
                 }

    def _ensure_query_integrity(self):
         """
         Ensures the query is complete and can be executed properly, raises error otherwise.
         Currently just checks that theres at least one filter.
         """

         if "query" not in self._query:
            raise CrunchbaseQueryError(f"Query must have at least 1 filter. Current query state: {self._query}")



