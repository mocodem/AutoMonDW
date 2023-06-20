from fetch_urls import extract_onion_addresses, extract_ahmia
from check_urls import access_url
from crawl import crawl
import oniondb
import elastico

import datetime
from time import sleep
import json
from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

with open("sources/seeds.json", "r") as f:
    sources = json.loads(f.read())

urls = extract_onion_addresses(sources.get("directories"))
urls += extract_ahmia("https://ahmia.fi:443/stats/static/data.json")

print("starting fetching onions")
for i,[url, source] in enumerate(urls):
    print("------------------------ "+str(i)+"/"+str(len(urls))+" ------------------------")
    print(url, "from", source)
    url = oniondb.sanitize_url(url)
    oniondb.add_onion(url, source)
    if oniondb.check_url_verison(url) != "v3":
        print(url, "is not v3, skipping")
        continue
    old_onion = oniondb.get_onion(url)
    if old_onion:
        if old_onion.status == 200:
            print(url, "already in db, fetching to copy data")
            current = oniondb.get_onion_source(url, source)
            current.status = old_onion.status
            current.captcha = old_onion.captcha
            current.captcha_type = old_onion.captcha_type
            current.save()
            continue
        elif old_onion.status == None:
            print(url, "already in db, but not requested")
            pass
        else:
            print(url, "already in db, server was down")
            continue
    print(url, "requesting...")
    status, captcha, captcha_type, data = access_url(url)
    current = oniondb.get_onion_source(url, source)
    current.status = status
    current.captcha = captcha
    current.captcha_type = captcha_type
    current.save()
    print(url, "with status:", status, "captcha:", captcha)
    if status == 200:
        oniondb.add_sitemap(url, url)
        es.index(index="onion_content", id=url, document={"url": url, "sitemap": url, "itc": str(datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')), "content": data.text})
        print(url, "added to elastico")
        continue
        sitemap = crawl(url, depth=1, data=data)
        print(len(sitemap), "--->", sitemap)
        for site in sitemap:
            if url in site:
                print(site)
                print(current)
                oniondb.add_sitemap(site, url)


print("done")
