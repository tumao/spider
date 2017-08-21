import requests
import pymysql
from selenium import webdriver
import time
from lxml import etree


driver = webdriver.PhantomJS("/usr/local/src/phantomjs/bin/phantomjs")

driver.set_page_load_timeout(10)
driver.set_script_timeout(10)
dcap["phantomjs.page.settings.loadImages"] = False
driver.get("http://hotels.ctrip.com/hotel/dianping/2707235_p3t0.html")
driver.implicitly_wait(5)
content = driver.find_element_by_class_name("comment_detail_list").text

print(content)
# file = open("asdfasd.txt", 'a', encoding='utf-8')
# file.write(content)
# file.close()
# end = time.time()
# print("用时："+str(end-start))
# content = driver.find_element_by_xpath("//div[@class='J_commentDetail']/text()")
# # content = driver.find_elements_by_class_name("J_commentDetail")
# selector = etree.HTML(content)
# result = selector.xpath("//div[@class='J_commentDetail']/text()")
# print(result)


driver.close()