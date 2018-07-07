import os
import time
import re
import json
import datetime

from selenium import webdriver
from pyvirtualdisplay import Display

import setting

# str(datetime.datetime.now()) + ' | ' +

class crawlers:
    def __init__(self, name, indexUrl):
        # 定義變數
        self.WEBDRIVER_PATH = os.environ.get('webdriver_path')
        self.DEPENDENCY_PATH = os.environ.get('dependency_path')
        self.DATA_PATH = os.environ.get('data_path')
        self.DATA_PATH = self.DATA_PATH + name + '/'
        self.JSON_PATH = self.DATA_PATH + 'menu.json'
        self.name = name
        self.indexUrl = indexUrl
        if not os.path.exists(self.DATA_PATH):
            print(str(datetime.datetime.now()) + ' | ' +
                  'not exists so make new dir , and this is the path : ' + self.DATA_PATH)
            os.mkdir(self.DATA_PATH)

    def update(self):
        print(str(datetime.datetime.now()) + ' | ' + self.name)

        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        option.add_argument('window-size=1920x1080')
        DRIVER = webdriver.Chrome(chrome_options=option, executable_path=self.DEPENDENCY_PATH+'headless_chromedriver')
        DRIVER.get(self.indexUrl + 'index.html')

        # 印出所有章節url
        CONTENTS = DRIVER.find_elements_by_css_selector('body > div:nth-child(5) > div.mainbody > div.centent > ul > li')
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

        if os.path.exists(self.JSON_PATH):
            # 舊章節json
            with open(self.JSON_PATH, 'r') as f:
                menuJson_old = json.load(f)
        else:
            menuJson_old = {}

        crawlJson = self.chapDiff(menuJson, menuJson_old)

        self.crawl(crawlJson, self.DATA_PATH, DRIVER)

        with open(self.JSON_PATH, 'w') as f:
            json.dump(menuJson, f)

        print(str(datetime.datetime.now()) + ' | ' +
              self.name + ' download complete ')

    def chapDiff(self, new, old):
        # print(self.indexUrl)
        returnJson = {}
        # returnIndex = 1

        for new_i in new:
            try:
                chap=old[str(new_i)]
            except (IndexError, KeyError):
                # print('There is no chapter('+str(new_i)+') in database')
                # print('So add in download')
                returnJson[new_i]=new[new_i]
                #returnJson.update({returnIndex: new[new_i]})
                #returnIndex = returnIndex + 1

        # print('new chapters :')
        print(*returnJson)
        return returnJson

    def crawl(self, sites, path, DRIVER):
        # print('this crawl')
        for index in sites:
            url = sites[index]['url']
            chapter = sites[index]['chapter']
            DRIVER.get(self.indexUrl + url)
            # 使用網頁的簡轉繁功能
            DRIVER.find_element_by_id('st').click()
            content = DRIVER.find_element_by_xpath('//*[@id="content"]').text
            # 檢查該路徑(DATA_PATH)下有無 index編號.md 無則創一個
            file = open(path + str(index) + '.txt', 'a')
            file.write(content)
            file.close()
            # print(str(datetime.datetime.now()) +
            #       ' | ' + chapter + ' download complete')
