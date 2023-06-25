from elasticsearch import Elasticsearch
import datetime

# Establish connection to Elasticsearch
es = Elasticsearch("http://localhost:9200")
try:
    # Check if Elasticsearch is successfully connected
    es.info()
    print("Elasticsearch successfully connected")
except:
    # If Elasticsearch is not connected, prompt user for input
    input("Elasticsearch is not connected, continue? ")

def create_mappings():
    # Define mappings for the index
    mappings = {
        "properties": {
            "url": {"type": "text", "analyzer": "standard"},
            "sitemap": {"type": "text", "analyzer": "standard"},
            "itc": {"type": "text", "analyzer": "standard"},
            "content": {"type": "text", "analyzer": "standard"}
        }
    }

    # Create the index with mappings
    es.indices.create(index="onion_content", mappings=mappings)

def search_content(q: str):
    print("-------------- search query: ", q, " --------------")
    a = datetime.datetime.now()

    # Perform a search query on the "content" field
    resp = es.search(index="onion_content", query={"match": {"content": q}}, size=100)
    print("query time:", datetime.datetime.now() - a)
    print("Got %d Hits:" % resp['hits']['total']['value'])

    # Iterate through the search results
    for i, hit in enumerate(resp['hits']['hits']):
        if hit["_score"] > 1.0:
            print("\n" + str(i + 1) + ":" + hit["_id"] + " -> Score: " + str(hit["_score"]))

def search_url(q: str):
    # Perform a search query on the "url" field
    resp = es.search(index="onion_content", query={"match": {"url": q}}, size=100)
    print("Got %d Hits:" % resp['hits']['total']['value'])

    # Iterate through the search results
    for i, hit in enumerate(resp['hits']['hits']):
        if hit["_score"] > 1.0:
            print("\n" + str(i + 1) + ":" + hit["_id"] + " -> Score: " + str(hit["_score"]))
            print(hit)

def get_by_id(id: str) -> dict:
    # Get a document by ID from the index
    resp = es.get(index="onion_content", id=id)
    print(resp['_source'])

# Perform search queries
# search_content("captcha")
# search_content("bypass")
