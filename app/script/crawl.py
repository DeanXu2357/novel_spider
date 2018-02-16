import os
import time
import re
import json

from selenium import webdriver
from pyvirtualdisplay import Display

import setting

class crawler:
    def __init__(self, name, indexUrl):
        # 定義變數
        self.WEBDRIVER_PATH = os.environ.get('webdriver_path')
        self.DATA_PATH = os.environ.get('data_path')
        self.DATA_PATH = self.DATA_PATH + name + '/'
        self.JSON_PATH = self.DATA_PATH + 'menu.json'
        self.name = name
        self.indexUrl = indexUrl

    def update(self):
        print(self.name)

        # open webdriver with no browser
        display = Display(visible=0, size=(800, 600))
        display.start()
        DRIVER = webdriver.Chrome(self.WEBDRIVER_PATH)
        DRIVER.get(self.indexUrl)
        CONTENTS = DRIVER.find_elements_by_css_selector('body > div:nth-child(5) > div.mainbody > div.centent > ul > li')

        # 印出所有章節url
        menuJson = {}
        menuIndex = 1
        for item in CONTENTS:
            data = item.get_attribute('innerHTML')
            matchObj = re.match('<a href="(.*?)">(.*?)</a>', data)
            if matchObj:
                # matchObj.group() 1：網址  2：章節名
                # print(matchObj.group(2) + ':' + matchObj.group(1))
                menuContent = {'chapter': matchObj.group(2), 'url': matchObj.group(1)}
                menuJson.update({menuIndex: menuContent})
                menuIndex = menuIndex + 1

        # 舊章節json
        with open(self.JSON_PATH, 'r') as f:
            menuJson_old = json.load(f)

        crawlJson = self.chapDiff(menuJson, menuJson_old)

        for index in crawlJson:
            url = crawlJson[index]['url']
            chapter = crawlJson[index]['chapter']
            DRIVER.get('http://www.piaotian.com/html/7/7580/' + url)
            # 使用網頁的簡轉繁功能
            DRIVER.find_element_by_id('st').click()
            content = DRIVER.find_element_by_xpath('//*[@id="content"]').text
            # 檢查該路徑(DATA_PATH)下有無 index編號.md 無則創一個
            file = open(self.DATA_PATH + str(index) + '.txt', 'a')
            file.write(content)
            file.close()
            print(chapter + ' download complete')

        print(self.name + ' download complete ')

    def chapDiff(self, new, old):
        print(self.indexUrl)
        returnJson = {}
        if len(new) > len(old):
            returnJson = new[len(old):]

        return returnJson
