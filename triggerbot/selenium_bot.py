
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
# macos
binary = "/Applications/Tor Browser.app/Contents/MacOS/firefox"
options.binary_location = binary
driver = webdriver.Firefox(options=options)

# linux
# binary = "/home/morty/tor-browser_en-US/Browser/firefox"
# firefox_binary = FirefoxBinary(binary)
# driver = webdriver.Firefox(firefox_binary=firefox_binary, options=options)


def run(onion: str):

    url = 'https://www.google.com/'
    url = 'https://icanhazip.com'  # it shows your IP
    # url = 'https://httpbin.org/get'  # it shows your IP and headers/cookies
    try:
        driver.get(onion)
        return 200
    except:
        return 0
