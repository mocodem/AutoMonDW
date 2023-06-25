import requests, re
from bs4 import BeautifulSoup
"""
proxies = {
    'http': 'socks5h://127.0.0.1:9150',
    'https': 'socks5h://127.0.0.1:9150'
}

# linux
"""
proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

# honeypot test to request all links
def run(onion: str):
    # request target
    content = requests.get(onion, proxies=proxies).content
    soup = BeautifulSoup(content, 'html.parser')
    # find all links
    links = soup.find_all('a')
    for link in links:
        try:
            href = link.get('href')
            if href and href.endswith('.onion/'):
                # request all links
                requests.get(href, proxies=proxies)
            elif href and href.startswith("/"):
                if onion.endswith("/"):
                    requests.get(onion[:-1]+href, proxies=proxies)
                requests.get(onion+href, proxies=proxies)
        except:
            pass
    # check if target still available
    if 200 == requests.get(onion, proxies=proxies).status_code:
        return False
    else:
        return True
