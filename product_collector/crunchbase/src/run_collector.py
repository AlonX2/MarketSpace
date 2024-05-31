import pika

from src.crunchbase_org import CrunchbaseOrganization
from src.crunchbase_query import CrunchbaseSearchQuery
from src.config import CRUNCHBASE_API_ENDPOINT
from utils import get_env_vars

def send_to_rabbit(content: str):
    """
    Sends a message with custom content to a rabbitmq queue, where the host, exchange and rk are dictated by env vars.
    :param content: The content to send to the rabbitmq queue.
    """
    
    host, exchange, routing_key = get_env_vars(["RABBIT_HOST", "RABBIT_EXCHANGE", "RABBIT_ROUTING_KEY"], 
                                               required=True)
    
    with pika.BlockingConnection(pika.ConnectionParameters(host=host)) as conn:
        channel = conn.channel()
        channel.basic_publish(exchange=exchange,
                              routing_key=routing_key,
                              body=content)

def get_orgs_by_categories(categories: list[str], start_date: str = None, end_date: str = None) -> list[dict]:
    """
    Searches crunchbase for organizaions in categories, with an option to filter by crunchbase registration dates.
    :param categories: The categories to find orgs in.
    :param start_date: Will only return orgs added to crunchbase after the given date.
                       The datetime should be of the following format "2015-02-02T23:00:05Z".
    :param end_date: Will only return orgs added to crunchbase before the date. 
                    The datetime should be of the following format "2015-02-02T23:00:05Z".
    :returns: List of org info dicts, for all organizations found. Refer to the crunchbase API docs for info on the dict format.
    """

    query_url = f"{CRUNCHBASE_API_ENDPOINT}/searches/organizations"
    query = CrunchbaseSearchQuery(query_url, requested_fields=CrunchbaseOrganization.required_fields)

    query.add_filter("categories", "Includes", categories)
    query.define_sorting("rank_org")

    if start_date is not None:
        query.add_filter("created_at", "gte", start_date)
    if end_date is not None:
        query.add_filter("created_at", "lte", end_date)            
    
    return query.execute()
        
def collect():
    """
    Starts collecting organizations from Crunchbase, categories and date limits dictated by env vars.
    Sends a message to rabbit queue for each org found.
    """

    org_categories, = get_env_vars(["CATEGORIES"], required=True)
    start_date, end_date = get_env_vars(["START_DATE", "END_DATE"])
    
    orgs =  get_orgs_by_categories(org_categories, start_date, end_date)
    for org_info in orgs:
        org = CrunchbaseOrganization.create_from_org_fields(org_info)
        send_to_rabbit(org.json())

if __name__ == "__main__":
    collect()