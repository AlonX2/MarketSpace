import pika

from product_scraper.crunchbase.src.crunchbase_org import CrunchbaseOrganization
from product_scraper.crunchbase.src.crunchbase_query import CrunchbaseSearchQuery
from product_scraper.crunchbase.src.exceptions import ScrapeException
from utils import get_env_vars

def send_to_rabbit(content):
    host, exchange, routing_key = get_env_vars(["RABBIT_HOST", "RABBIT_EXCHANGE", "RABBIT_ROUTING_KEY"], 
                                               required=True)
    with pika.BlockingConnection(pika.ConnectionParameters(host=host)) as conn:
        channel = conn.channel()
        channel.basic_publish(exchange=exchange,
                              routing_key=routing_key,
                              body=content)

def get_top_orgs_by_categories(categories, start_date = None, end_date = None):
    query_url = "https://api.crunchbase.com/api/v4/searches/organizations"
    query = CrunchbaseSearchQuery(query_url, requested_fields=CrunchbaseOrganization.required_fields)

    query.add_filter("categories", "Includes", categories)
    query.define_sorting("rank_org")

    if start_date is not None:
        query.add_filter("created_at", "gte", start_date)
    if end_date is not None:
        query.add_filter("created_at", "lte", end_date)            
    
    return query.execute()
        
def run_scraper():
    org_categories, = get_env_vars(["CATEGORIES"], required=True)
    start_date, end_date = get_env_vars(["START_DATE", "END_DATE"])

    if org_categories is None:
        raise ScrapeException("Missing required environment variable 'CATEGORIES'.")
    
    orgs =  get_top_orgs_by_categories(org_categories, start_date, end_date)
    for org_info in orgs:
        org = CrunchbaseOrganization.create_from_org_fields(org_info)
        send_to_rabbit(org.json())

if __name__ == "__main__":
    run_scraper()