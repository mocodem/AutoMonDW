import requests
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
# Establih the proxy connection by finding the correct open tor port using: sudo lsof -i -n -P | grep TCP
# macos

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
"""
def run(onion: str):
    return requests.get(onion, proxies=proxies).status_code
