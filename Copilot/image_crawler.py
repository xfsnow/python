# using selenium and chromedriver as headless browser
# go to https://azure.microsoft.com/
# window size 1920*1080
# sleep for 3 seconds
# save screenshot as current timestamp.png
# close browser

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import datetime

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get("https://azure.microsoft.com/")
time.sleep(3)
driver.save_screenshot(datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".png")
driver.close()