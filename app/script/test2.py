import os
import time
import re
import json

from selenium import webdriver

import setting

# 定義變數
WEBDRIVER_PATH = os.environ.get('webdriver_path')
DATA_PATH = os.environ.get('data_path')
NOVEL_NAME = '極道天魔'
DATA_PATH = DATA_PATH + NOVEL_NAME + '/'
if not os.path.exists(DATA_PATH):
    print('not exists so make new dir , and this is the path : ' + DATA_PATH)
    os.mkdir(DATA_PATH)

JSON_PATH = DATA_PATH + 'menu.json'

# 極道天魔目錄頁
# TODO 未來應該建立一個 {小說: 目錄頁} mapping的json 專門給飄天文學網
DRIVER = webdriver.Chrome(WEBDRIVER_PATH)

DRIVER.get('http://www.piaotian.com/html/8/8502/5379303.html')

content = DRIVER.find_element_by_xpath(
    '//*[@id="content"]').get_attribute('innerHTML')

print(content)

DRIVER.close()

