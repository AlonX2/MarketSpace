import os, requests

from product_scraper.crunchbase_org import CrunchbaseOrganization

PAGINATION_BATCH_SIZE = 500
class CrunchbaseScrape():
    def __init__():
        pass
    
    def run():
        pass
    
    def _paginate_search_query(self, url, query, desired_count):
        api_key = os.getenv("CRUNCHBASE_API_KEY")
        entities = []

        while desired_count > 0:
            query_count = min(PAGINATION_BATCH_SIZE, desired_count)
            query["count"] = query_count

            if len(entities) > 0:
                previous_item_id = entities[-1]["uuid"]
                query["after_id"] = previous_item_id

            resp = requests.post(url, params={"user_key": api_key}, json=query)
            if not resp.status_code == 200:
                raise requests.exceptions.RequestException(f"Failed to perform query, got status code {resp.status_code}")
            
            content = resp.json()
            desired_count -= content["count"]
            entities.extend(content["entities"])
        
        return entities

    def _get_top_orgs_in_category(self, categories, count = 1000):
        query = {"field_ids": CrunchbaseOrganization.required_fields, 
                 "query": [{
                     "type": "predicate",
                     "field_id": "categories",
                     "operator_id": "Includes",
                     "values": categories
                 }],
                 "order": [{
                     "field_id": "rank_org",
                     "sort": "desc"
                 }],
                 "limit": min(PAGINATION_BATCH_SIZE, count)}
        
        orgs = self._paginate_search_query("https://api.crunchbase.com/api/v4/searches/organizations", query, count)
            
    
