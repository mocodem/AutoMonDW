import requests
import json

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

def access_url(url: str) -> (int, bool, str, requests.models.Response):
    try:
        # Access the URL using Tor proxy
        data = requests.get(url, proxies=proxies)
        captcha = False
        captcha_type = None

        # Check for captcha presence in the response content
        if "captcha" in str(data.content) or "bypass" in str(data.content):
            captcha = True
            captcha_type = "undetected"

        return data.status_code, captcha, captcha_type, data
    except requests.exceptions.ConnectionError:
        print(url, "server not responding")
        return 400, None, None, None
    except Exception as e:
        print(e)
        print(f"error from {url}")
        return None, None, None, None


def get_content(url: str) -> (int, bool, str):
    try:
        # Get the content of the URL using Tor proxy
        content = requests.get(url, proxies=proxies)
        return content
    except Exception as e:
        print(e)
        print(f"error from {url}")
        return None

def tor_connection() -> bool:
    try:
        # Check if the IP address is different when using Tor proxy and without
        if json.loads(requests.get('http://httpbin.org/ip', proxies=proxies).text)["origin"] != json.loads(requests.get('http://httpbin.org/ip').text)["origin"]:
            return True
        else:
            return False
    except:
        return False

# Check if Tor is connected
if not tor_connection():
    input("TOR is not connected, continue? ")
else:
    print("TOR successfully connected")
