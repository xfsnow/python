# 使用 selenium 配合 chromedriver 作为浏览器，抓取网页内容
# 访问 https://azure.microsoft.com/zh-cn/products/
# 保存截图为当前年月日时分秒.png
# 关闭浏览器
# 把截图转换为灰度图，再以当前的年月日时分秒加 _ 加 gray 为文件名保存

from selenium import webdriver
from datetime import datetime
import time
from PIL import Image

# 1. 创建浏览器对象
driver = webdriver.Chrome()

# 2. 访问网页
driver.get('https://azure.microsoft.com/zh-cn/products/')
time.sleep(3)

# 3. 截图
now = datetime.now()
filename = now.strftime('%Y%m%d%H%M%S') + '.png'
driver.save_screenshot(filename)

# 4. 关闭浏览器
driver.quit()

# 5. 把截图转换为灰度图
img = Image.open(filename)
img = img.convert('L')
filename = now.strftime('%Y%m%d%H%M%S') + '_gray.png'
img.save(filename)