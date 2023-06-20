
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
options = webdriver.ChromeOptions()
options.add_argument("--tor")
# linux
# driver = uc.Chrome(version_main=113, browser_executable_path='/usr/bin/brave-browser', options=options)
# macos
driver = uc.Chrome(version_main=113, browser_executable_path='/Applications/Brave Browser.app/Contents/MacOS/Brave Browser', options=options)
def run(onion: str):
    try:
        driver.get(onion)
        try:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='proceed-button']"))).click()
        except:
            pass
        return 200
    except:
        return 0
