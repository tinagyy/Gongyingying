# encoding=utf-8
from selenium import webdriver
import time
driver = webdriver.Firefox(executable_path = "E:\\geckodriver")
driver.get("https://www.baidu.com")
driver.find_element_by_id("kw").clear()
driver.find_element_by_id("kw").send_keys(u"软件测试")
driver.find_element_by_id("su").click()
time.sleep(3)
driver.quit()

