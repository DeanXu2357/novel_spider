from selenium import webdriver
#from selenium.webdriver.chrome.options import options
import os

#chrome_options = Options()
#chrome_options.add_argument("--headless")
#chrome_options.add_argument("--window-size=1920x1080")
option = webdriver.ChromeOptions()
option.add_argument('headless')
option.add_argument('window-size=1920x1080')

chrome_driver = "./headless_chromedriver"

# go to Google and click the I'm Feeling Lucky button
driver = webdriver.Chrome(chrome_options=option, executable_path=chrome_driver)
driver.get("https://www.google.com")
lucky_button = driver.find_element_by_css_selector("[name=btnI]")
lucky_button.click()

# capture the screen
driver.get_screenshot_as_file("capture.png")
