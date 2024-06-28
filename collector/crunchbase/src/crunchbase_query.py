import requests, logging

from src.exceptions import CrunchbaseQueryError
from utils import get_env_vars

PAGINATION_BATCH_SIZE = 500

logger = logging.getLogger(__package__)

class CrunchbaseSearchQuery():
    """
    Class for building and executing crunchbase search queries.
    """

    def __init__(self, url: str, requested_fields: list[str]):
        """
        Intializer for the class.
        :param url: The url to query from.
        :param requested_fields: The fields the query should request to receive for every found entity in the search.
        """

        if len(requested_fields) == 0:
            raise CrunchbaseQueryError(f"Query must have at least 1 requested field. Got the following fields list: {requested_fields}")
        
        self._url = url
        self._query = {"field_ids": requested_fields}

        logger.debug(f"Initialized crunchbase query object with url '{url}' with requested fields '{requested_fields}'.")

    def execute(self) -> list[dict]:
        """
        Execute the query with pagination until theres no more results.
        :returns: List of all returned entities.
        """

        api_key, = get_env_vars(["CRUNCHBASE_API_KEY"], required=True)

        self._ensure_query_integrity()

        executing_query = self._query.copy()
        executing_query["limit"] = PAGINATION_BATCH_SIZE

        logger.info("Starting to execute query")
        logger.debug(f"Executing query state: {executing_query}")

        entities = []
        while True:
            if len(entities) > 0:
                previous_item_id = entities[-1]["uuid"]
                executing_query["after_id"] = previous_item_id
            
            content = self._perform_request(api_key, executing_query)

            logger.info(f"Got {len(content['entities'])} entities from crunchbase.")

            entities.extend(content["entities"])
            if len(content["entities"]) < PAGINATION_BATCH_SIZE:
                logger.info(f"Finished exectuting query, got {len(entities)} results.")
                break

        return entities

    def add_filter(self, field_name: str, operator: str, filter_value: str | list):
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

        logger.debug(f"Added filter '{filter}' to query. Current query state: '{self._query}'.")

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
        
        logger.debug(f"Added sorting by '{key_field}' to query. Current query state: '{self._query}'.")

    def _ensure_query_integrity(self):
         """
         Ensures the query is complete and can be executed properly, raises error otherwise.
         Currently just checks that theres at least one filter.
         """

         if "query" not in self._query:
            raise CrunchbaseQueryError(f"Query must have at least 1 filter. Current query state: {self._query}")

    def _perform_request(self, api_key: str, query: dict) -> dict:
        """
        Performs a request to crunchbase to fetch search query results. Raises CrunchbaseQueryError on error.
        :param api_key: A valid crunchbase api to perform the query with.
        :param query: The search query dict to perform.
        :returns: The response dict.
        """
        try:
            logger.debug(f"About to perform request to crunchbase, with url '{self._url}' and query '{query}'.")
            resp = requests.post(self._url, params={"user_key": api_key}, json=query)
        except requests.exceptions.RequestException as e:
            raise CrunchbaseQueryError(f"Failed to perform query due to requests error.") from e
            
        resp_data = resp.json()

        if resp.status_code != 200:
            raise CrunchbaseQueryError(f"Failed to perform query, got status code {resp.status_code}, content '{resp_data}'")
        

        logger.debug(f"Performed request to crunchbase, got {resp_data}")

        return resp.json()