import time
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

# Establih the proxy connection by finding the correct open tor port using: sudo lsof -i -n -P | grep TCP
# macos

proxy = Proxy({
    'proxyType': ProxyType.MANUAL,
    'socksProxy': '127.0.0.1:9150',
    'socksVersion': 5,
})

# linux
"""
proxy = Proxy({
    'proxyType': ProxyType.MANUAL,
    'socksProxy': '127.0.0.1:9050',
    'socksVersion': 5,
})
"""
options = Options()
options.proxy = proxy

# initiate driver to spawn browser

# macos
binary = "/Applications/Tor Browser.app/Contents/MacOS/firefox"
options.binary_location = binary
driver = webdriver.Firefox(options=options)

# linux
# binary = "/home/morty/tor-browser_en-US/Browser/firefox"
# firefox_binary = FirefoxBinary(binary)
# driver = webdriver.Firefox(firefox_binary=firefox_binary, options=options)


def run(onion: str, cookies = None):
    # add cookies if needed
    if cookies:
        for cookie in cookies:
            driver.add_cookie(cookie)
    try:
        # request target
        driver.get(onion)
        return 200
    except:
        return 0


def get_cookies(onion: str):
    print("sleeping 10 sec")
    time.sleep(10)
    driver.get(onion)
    input("solve captcha: ")
    all_cookies=driver.get_cookies();
    cookies_dict = {}
    for cookie in all_cookies:
        cookies_dict[cookie['name']] = cookie['value']
    print(cookies_dict)
    return cookies_dict
