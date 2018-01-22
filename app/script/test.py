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
DRIVER.get('http://www.piaotian.com/html/8/8502/index.html')

CONTENTS = DRIVER.find_elements_by_css_selector(
    'body > div:nth-child(5) > div.mainbody > div.centent > ul > li')

menuJson = {}
menuIndex = 1
# 印出所有章節url
for item in CONTENTS:
    data = item.get_attribute('innerHTML')
    matchObj = re.match('<a href="(.*?)">(.*?)</a>', data)
    if matchObj:
        # matchObj.group() 1：網址  2：章節名
        # print(matchObj.group(2) + ':' + matchObj.group(1))
        menuContent = {'chapter': matchObj.group(2), 'url': matchObj.group(1)}
        menuJson.update({menuIndex:menuContent})
        menuIndex = menuIndex + 1

with open(JSON_PATH, 'w') as f:
    json.dump(menuJson, f)

# TODO 這邊可能要研究一下 generate 或是 多線程
# menuJson 用鍵排序
# 迴圈
# 前往該url
# 抓取內容
# 寫到dir 用menuJson鍵作檔案名 寫成md檔


# 搜尋列輸入
# driver.find_element_by_xpath('//*[@id="searchkey"]').send_keys('極道天魔')
# 搜尋列按下確定
# driver.find_element_by_name('Submit').click()
# time.sleep(1)

# 暫停三秒
time.sleep(1)

DRIVER.close()
