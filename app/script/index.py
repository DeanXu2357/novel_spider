import os
import time

from selenium import webdriver

import setting

webdriver_path=os.environ.get('webdriver_path')

driver=webdriver.Chrome(webdriver_path)
driver.get("https://google.com")

# 暫停三秒
time.sleep(3)

driver.close()