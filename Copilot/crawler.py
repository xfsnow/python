# 使用 selenium 配合 chromedriver 作为无窗口浏览器，抓取网页内容
# 访问 https://azure.microsoft.com/zh-cn/products/
# 抓取所有class="text-heading5"的h3标签，以及其后面class="text-body4"的p标签
# 退出浏览器
# 提取出文本，整理成表格，输出成CSV文件
# 保存文本为当前年月日时分秒.csv
# 关闭文件

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import csv

# 无窗口模式
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

# 启动浏览器
browser = webdriver.Chrome(options=chrome_options)
browser.get('https://azure.microsoft.com/zh-cn/products/')
time.sleep(3)

# 抓取数据
h3s = browser.find_elements(By.CLASS_NAME, 'text-heading5')
ps = browser.find_elements(By.CLASS_NAME, 'text-body4')

# 整理数据
data = []
for i in range(len(h3s)):
    data.append([h3s[i].text, ps[i].text])


# 保存数据
with open(time.strftime('%Y%m%d%H%M%S', time.localtime()) + '.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(data)

# 关闭浏览器
browser.quit()