# 單頁爬取＆寫入檔案
import os
import time
import re
import json
from pprint import pprint

from selenium import webdriver
import opencc

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

DRIVER = webdriver.Chrome(WEBDRIVER_PATH)

DRIVER.get('http://www.piaotian.com/html/8/8502/5379303.html')

content = DRIVER.find_element_by_xpath(
    '//*[@id="content"]').text

# contents = DRIVER.find_elements_by_css_selector('#content > font')
conv_content = opencc.convert(content, config='s2t.json')
print(conv_content)
# pprint(content)


# print(content)

DRIVER.close()
