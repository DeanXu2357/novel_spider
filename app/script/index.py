#!/usr/bin/python3
import os
import time
import sys
import json
import datetime

from selenium import webdriver

import setting
from crawl import crawlers

DATA_PATH = os.environ.get('data_path')
# print(DATA_PATH)
INDEX_PATH = DATA_PATH + 'index.json'

if not os.path.exists(INDEX_PATH):
    with open(INDEX_PATH, 'w') as f:
        json.dump({}, f)

with open(INDEX_PATH, 'r') as f:
    indexJson = json.load(f)

# 根據傳進來的參數
mainAct = sys.argv[1]
if mainAct == 'list':
    if len(sys.argv) >= 3:
        subAct = sys.argv[2]

        if subAct == 'add':
            if len(sys.argv) < 6:
                print(str(datetime.datetime.now()) +
                      ' | ' + 'error : args not found')
                exit(0)

            novelName = sys.argv[3]
            index = len(indexJson) + 1
            additionalContent = {
                'name': novelName,
                'source': {
                    1:{
                        'name': sys.argv[4],
                        'url': sys.argv[5]
                    }
                }
            }

            indexJson.update({index: additionalContent})

            print(str(datetime.datetime.now()) +
                  ' | ' + 'book list update complete')
        elif subAct == 'rm':
            indexJson.pop(sys.argv[3])
            print(str(datetime.datetime.now()) + ' | ' + 'remove complete')
        else:
            print(str(datetime.datetime.now()) +
                  ' | ' + subAct + ': command not found')

        with open(INDEX_PATH, 'w') as f:
            json.dump(indexJson, f)
    else:
        print(indexJson)
elif mainAct == 'crawl':
    start = time.perf_counter()

    for index in indexJson:
        crawler = crawlers(
            indexJson[str(index)]['name'],
            indexJson[str(index)]['source']['1']['url']
        )
        crawler.update()

    print(str(datetime.datetime.now()) + ' | ' +
          '總執行時間:', time.perf_counter() - start)
    print(str(datetime.datetime.now()) + ' | ' +
          'All Complete !!')
else:
    print(str(datetime.datetime.now()) + ' | ' +
          mainAct + ': command not found')

# list add
# 新增 書籍＆index url

# list
# 顯示Data書籍列表

# list rm
# 刪除Data書籍列表該 by書籍id

# crawl - 讀取Data書籍列表
# 迴圈依照列表爬取
#     基本test.py內容＋判斷章節是否爬取過
#     + xxx 已爬取完畢 or 更新章節完畢

# 輸出 運行完畢
