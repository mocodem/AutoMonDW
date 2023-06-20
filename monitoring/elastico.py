from elasticsearch import Elasticsearch
import datetime

es = Elasticsearch("http://localhost:9200")
# print(es.info().body)
try:
    es.info()
    print("Elasticsearch successfully connected")
except:
    input("Elasticsearch is not connected, continue? ")

def create_mappings():
    mappings = {
            "properties": {
                "url": {"type": "text", "analyzer": "standard"},
                "sitemap": {"type": "text", "analyzer": "standard"},
                "itc": {"type": "text", "analyzer": "standard"},
                "content": {"type": "text", "analyzer": "standard"}
        }
    }

    es.indices.create(index="onion_content", mappings=mappings)

def search_content(q: str):
    print("-------------- search query: ",q, " --------------")
    a = datetime.datetime.now()
    resp = es.search(index="onion_content", query={"match": {"content": q}}, size=100)
    print("query time:", datetime.datetime.now()-a)
    print("Got %d Hits:" % resp['hits']['total']['value'])
    for i, hit in enumerate(resp['hits']['hits']):
        if hit["_score"] > 1.0:
            print("\n" + str(i+1) + ":" + hit["_id"] + " -> Score: " + str(hit["_score"]))
        # print(hit["_source"]["content"][:10])
        #print(hit)

def search_url(q: str):
    resp = es.search(index="onion_content", query={"match": {"url": q}}, size=100)
    print("Got %d Hits:" % resp['hits']['total']['value'])
    for i, hit in enumerate(resp['hits']['hits']):
        if hit["_score"] > 1.0:
            print("\n" + str(i+1) + ":" + hit["_id"] + " -> Score: " + str(hit["_score"]))
            print(hit)

def get_by_id(id: str) -> dict: #{url, sitemap, itc, content}
    resp = es.get(index="onion_content", id=id)
    print(resp['_source'])


search_content("captcha")
search_content("bypass")



