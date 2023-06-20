import requests.models
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from check_urls import get_content


def crawl(url: str, depth: int = 1, data: requests.models.Response = None) -> list[str]:
    crawled = []
    indexed_url = [url]
    collected_url = []
    for i in range(depth):
        for page in indexed_url:
            if page not in crawled:
                crawled.append(page)
                if data and data.url == page:
                    content = data
                else:
                    content = get_content(page)
                if not content:
                    print("Could not open %s" % page)
                    continue
                soup = BeautifulSoup(content.text, "lxml")
                links = soup('a')
                for link in links:
                    if 'href' in dict(link.attrs):
                        url = urljoin(page, link['href'])
                        if url.find("'") != -1:
                            continue
                        url = url.split('#')[0]
                        if url[0:4] == 'http':
                            collected_url.append(url)
        indexed_url = indexed_url + collected_url
    return list(set(indexed_url))
