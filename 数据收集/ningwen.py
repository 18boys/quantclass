from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from datetime import datetime
import pandas as pd
import os
import random

# 自动获取宁稳网可转债全表数据
# 使用前提条件：
# 1.电脑已经安装chrome
# 自行搜索下载
# 2.安装对应chrome版本的的chromedriver
# mac系统对应106.0.5249.61版本的chromedriver
# wget http://chromedriver.storage.googleapis.com/106.0.5249.61/chromedriver_mac64.zip
# 通过wget下载之后，放置在系统的path路径内（不懂path的可以搜索 ）
# 3.通过chrome手动访问宁稳网的下面链接，保证手动访问可以正常访问
# 访问https://www.ninwin.cn/index.php?m=cb&a=cb_all&show_cb_only=Y&show_listed_only=Y
# 这一步主要保证登录等状态是正常的，如果手动访问都异常，那么脚本也获取不到数据
# 注意：宁稳网访问可转债数据需要通过题目测试才行

# 本地chrome debug端口
port = '9645'
# chrom本地启动命令路径
chromeCmdPath = '/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome'
# 复用本地浏览器
os.system(f'{chromeCmdPath} --remote-debugging-port={port}')

chrome_options = Options()
# 全表
url = 'https://www.ninwin.cn/index.php?m=cb&a=cb_all&show_cb_only=Y&show_listed_only=Y'
# 简表
# url = 'https://www.ninwin.cn/index.php?m=cb&show_cb_only=Y&show_listed_only=Y'

# 增加无头（不打开浏览器）
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

# 防止被网站识别（伪装）
# chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
# 使用本地浏览器代理，复用cookie
chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")

service = Service(executable_path=ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=chrome_options)

browser.get(url)
# browser.maximize_window()
browser.implicitly_wait(1)

df = pd.read_html(
    browser.page_source,
    attrs={
        'id': 'cb_hq'
    },
)[0]

df = pd.DataFrame(df)
del df['转债名称.1']
del df['序号']

now = datetime.now()
dataStr = now.strftime('%Y-%m-%d')
dataStr = '2022-10-26'
df['日期'] = dataStr
df = df.set_index(['日期'])
print(df)

# 备份今日总表
os.system(f'cp ./data/all_date.csv ./data/all_date_{random.randint(1,999999)}.csv')
# 备份今日数据
df.to_csv(f'./data/single_date_{dataStr}.csv', mode='a')
# 写入总表
df.to_csv(f'./data/all_date.csv', mode='a', header=False)
# 复制今日总表
os.system(f'cp ./data/all_date.csv ./data/all_date_{dataStr}.csv')

