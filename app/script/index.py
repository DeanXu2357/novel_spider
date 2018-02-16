import os
import time
import sys
import json

from selenium import webdriver

import setting

DATA_PATH = os.environ.get('data_path')
INDEX_PATH = DATA_PATH + 'index.json'

# 根據傳進來的參數
mainAct = sys.argv[1]
if mainAct == 'list':
    if not os.path.exists(INDEX_PATH):
        with open(INDEX_PATH, 'w') as f:
            json.dump({}, f)

    with open(INDEX_PATH, 'r') as f:
        indexJson = json.load(f)

    if len(sys.argv) >= 3:
        subAct = sys.argv[2]

        if subAct == 'add':
            print('do list add')
            if len(sys.argv) < 6:
                print('error : args not found')
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
        elif subAct == 'rm':
            indexJson.pop(sys.argv[3])
            print('remove complete')
        else:
            print(subAct + ': command not found')

        with open(INDEX_PATH, 'w') as f:
            json.dump(indexJson, f)
    else:
        print(indexJson)
elif mainAct == 'crawl':
    print('do crawl')
else:
    print(mainAct + ': command not found')

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
