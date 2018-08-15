import os
import time
import re
import json
import datetime
import threading
from queue import Queue

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
        self.crawlQueue = Queue()
        if not os.path.exists(self.DATA_PATH):
            print(str(datetime.datetime.now()) + ' | ' +
                  'not exists so make new dir , and this is the path : ' + self.DATA_PATH)
            os.mkdir(self.DATA_PATH)

    def update(self):
        start = time.perf_counter()
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

        DRIVER.quit()

        crawlJson = self.chapDiff(menuJson, menuJson_old)

        if len(crawlJson) > 1:
            print('新內容：')
            print(*crawlJson)
            self.crawl(crawlJson, self.DATA_PATH)

        with open(self.JSON_PATH, 'w') as f:
            json.dump(menuJson, f)

        print(str(datetime.datetime.now()) + ' | ' +
               '單本執行時間:', time.perf_counter() - start)
        print(str(datetime.datetime.now()) + ' | ' + 'complete ')

    def chapDiff(self, new, old):
        returnJson = {}

        for new_i in new:
            try:
                chap=old[str(new_i)]
            except (IndexError, KeyError):
                returnJson[new_i]=new[new_i]

        return returnJson

    # 根據sites 迴圈爬取目標內容
    def crawl(self, sites, path):
        if len(sites) < 10:
            threadNum = 1
        elif len(sites) > 100:
            threadNum = 8
        else:
            threadNum = 4

        # creating a thread pool
        for i in range(threadNum):
            t = threading.Thread(target=self.crawlWorker, args=(sites, path))
            t.daemon = True
            t.start()

        # add sites to queue 將所有欲爬取的目標加到對列
        start = time.perf_counter()
        for item in sites:
            self.crawlQueue.put(item)

        self.crawlQueue.join()
        print('Crawl Time:', time.perf_counter() - start)

    # 爬取的worker
    def crawlWorker(self, sites, basicPath):
        while True:
            # 初始化webdriver
            option = webdriver.ChromeOptions()
            option.add_argument('headless')
            option.add_argument('window-size=1920x1080')
            Driver = webdriver.Chrome(chrome_options=option, executable_path=self.DEPENDENCY_PATH+'headless_chromedriver')

            # 根據queue爬取對應資料
            target = self.crawlQueue.get()
            url = sites[target]['url']
            self.crawlByUrl(url, target, basicPath, Driver)
            self.crawlQueue.task_done()

            Driver.close()

    # 爬取單頁
    def crawlByUrl(self, url, fileName, basicPath, Driver):
        Driver.get(self.indexUrl + url)
        # 使用網頁的簡轉繁功能
        Driver.find_element_by_id('st').click()
        content = Driver.find_element_by_xpath('//*[@id="content"]').text
        # 檢查該路徑(DATA_PATH)下有無 index編號.md 無則創一個
        file = open(basicPath + str(fileName) + '.txt', 'a')
        file.write(content)
        file.close()

