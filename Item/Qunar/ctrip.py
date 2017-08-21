from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree

dcap = dict(DesiredCapabilities.PHANTOMJS)
# print(dcap)
# #从USER_AGENTS列表中随机选一个浏览器头，伪装浏览器
# dcap["phantomjs.page.settings.userAgent"] = (base_controller.chooseagent())
# # 不载入图片，爬页面速度会快很多
dcap["phantomjs.page.settings.loadImages"] = False
# # 设置代理
# # service_args = ['--proxy=127.0.0.1:9999','--proxy-type=socks5']
# #打开带配置信息的phantomJS浏览器
# driver = webdriver.PhantomJS("/workplace/phantomjs/bin/phantomjs", desired_capabilities=dcap)
# # # 隐式等待5秒，可以自己调节
#
# driver.implicitly_wait(5)
# # # 设置10秒页面超时返回，类似于requests.get()的timeout选项，driver.get()没有timeout选项
# # # 以前遇到过driver.get(url)一直不返回，但也不报错的问题，这时程序会卡住，设置超时选项能解决这个问题。
# driver.set_page_load_timeout(10)
# # # 设置10秒脚本超时时间
# driver.set_script_timeout(10)

# driver.get("https://hotels.ctrip.com/hotel/2707235.html?isFull=F#ctm_ref=hod_sr_lst_dl_n_1_1")
# driver.find_elements_by_xpath("//div[@class='c_page_list layoutfix']//a")[2].click()
# driver.
# # print(driver.find_elements_by_xpath("//div[@class='c_page_list layoutfix']//a")[2].text)
# content = driver.find_elements_by_xpath("//div[@class='J_commentDetail']")
#
# print(content[1].text)
# file = open("tt1.txt", 'a')
# for i in range(len(content)):
#     print(content[i].text)
#     file.write(content[i].text)
#     file.write("\n")
# file.close()

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])                        # 屏蔽掉浏览器的认证错误
options.add_experimental_option('prefs', {"profile.managed_default_content_settings.images":2})         # 使chrome 浏览器不加载图片信息
chrome = webdriver.Chrome(executable_path="/usr/bin/chromedriver", chrome_options=options, desired_capabilities=dcap)
chrome.get("http://hotels.ctrip.com/hotel/432263.html?isFull=F#ctm_ref=hod_sr_lst_dl_n_1_3")
time.sleep(30)
xpath = "//div[@class='c_page']//a[@value="+str(5)+"]"
# WebDriverWait(chrome, 15).until(EC.invisibility_of_element_located((By.CLASS_NAME, "c_page")))
chrome.find_element_by_xpath(xpath=xpath).click()
time.sleep(20)
source = chrome.page_source

selector = etree.HTML(source)
content = selector.xpath("//div[@class='J_commentDetail']/text()")
for line in content:
    print("~~~~~~~~~")
    print(line)

file = open("pagesource.html", 'a', encoding='utf-8')
file.write(source)
file.close()

# content = chrome.find_elements_by_xpath("//div[@class='J_commentDetail']")
# print(content[1].text)
# file = open("tt1.txt", 'a')
# for i in range(len(content)):
#     print(content[i].text)
#     file.write(content[i].text)
#     file.write("\n")
# file.close()

chrome.close()