# 使用 selenium 配合 chromedriver 作为无窗口浏览器，抓取网页
# 访问 https://azure.microsoft.com/zh-cn/products/
# 保存截图为当前年月日时分秒.png
# 关闭浏览器
# 把截图转换为灰度图，再以当前的年月日时分秒加 _ 加 gray 为文件名保存


from selenium import webdriver
from PIL import Image
import time

driver = webdriver.Chrome()
driver.get('https://azure.microsoft.com/zh-cn/products/')
time.sleep(3)

timestamp = time.strftime('%Y%m%d%H%M%S')
driver.save_screenshot(timestamp + '.png')
driver.quit()

im = Image.open(timestamp + '.png')
im = im.convert('L')
im.save(timestamp + '_gray.png')
