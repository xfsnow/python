# 使用 selenium 配合 chromedriver 作为浏览器，获取网页快照
# 访问 https://azure.microsoft.com
# 窗口尺寸为 1920x1080
# 休眠 3 秒
# 保存截图为当前年月日时分秒.png
# 关闭浏览器

from selenium import webdriver
from time import sleep
from datetime import datetime

driver = webdriver.Chrome()
driver.get('https://azure.microsoft.com')
driver.set_window_size(1920, 1080)
sleep(3)
driver.save_screenshot(datetime.now().strftime('%Y%m%d%H%M%S') + '.png')
driver.quit()