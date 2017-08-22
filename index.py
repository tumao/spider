# -*- coding: utf-8 -*-
from Configs import conf_mysql
from Configs import conf_redis
from Configs import conf_log
from Engines.Controller import base_controller
import os
import requests
import pymysql
from lxml import etree
import json
import fileinput
from selenium import webdriver
import time
import selenium.common.exceptions
from selenium.common.exceptions import NoSuchElementException

conf_mysql = conf_mysql.mysql
conf_redis = conf_redis.redis

# if conf_log.is_save_log == True:
#     if os.path.exists(conf_log.log_dir) == False:
#         os.mkdir(conf_log.log_dir)


agent = base_controller.chooseagent()
headers = {
    "Accept":"text/html,application/xhtml+xml,application/xml;",
    "Accept-Encoding":"gzip",
    "Accept-Language":"zh-CN,zh;q=0.8",
    "Referer":"http://www.example.com/",
    "User-Agent":agent
    }

# ht_list_url = "http://hotels.ctrip.com/Domestic/Tool/AjaxHotelList.aspx"
# ht_sum_page = 2
#
conn = pymysql.connect(host=conf_mysql['host'], port=int(conf_mysql['port']), user=conf_mysql['user'], db=conf_mysql['db'], charset=conf_mysql['charset'], password=conf_mysql['passwd'])
cursor = conn.cursor()

"""download hotel info"""
# for x in range(ht_sum_page):
#     data = {"cityId": 34, "star": 5, "page": int(x+1)}  # 34 kunming
#     resource = requests.post(ht_list_url, data = data, headers = headers)
#     content = resource.content.decode("utf-8")
#     jsonContent = json.loads(content)
#     ht_content = jsonContent['hotelMapStreetJSON']
#     for k in jsonContent['hotelMapStreetJSON']:
#         ht_id = k
#         ht_name = ht_content[k]['amap']['fullname']
#         position = ht_content[k]['soso']['pos']
#         sql = "INSERT INTO `hotel_info` (`web_id`, `ht_id`, `ht_name`, `star`, `location`, `site_info`) VALUES(%d, %d, '%s', '5', '%s', '%s')"
#         data = (1, int(ht_id), ht_name, position, ' ')
#         cursor.execute(sql%data)
#         conn.commit()
#


"""download comments by hotel"""
cursor.execute("SELECT * FROM `hotel_info` WHERE `ht_id` > 438000 ORDER BY `ht_id`")
conn.commit()

for ht in cursor.fetchall():
    ht_id = ht[2]       # hotel的id
    url = "http://hotels.ctrip.com/hotel/dianping/"+str(ht_id)+"_p1t0.html"
    resource = requests.get(url, headers=headers)
    content = resource.content.decode("utf-8")
    selector = etree.HTML(content)
    ccount_tag = selector.xpath("//span[@id='All_Comment']/text()")
    ccount = ccount_tag[0].strip("全部(").strip(")")

    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])  # 屏蔽掉浏览器的认证错误
    options.add_experimental_option('prefs', {"profile.managed_default_content_settings.images": 2})  # 使chrome 浏览器不加载图片信息
    driver = webdriver.Chrome("/usr/bin/chromedriver", chrome_options=options)          # 通过驱动打开浏览器

    comment_url = "http://hotels.ctrip.com/hotel/dianping/" + str(ht_id) + "_p1t0.html"  # 某个酒店
    driver.get(comment_url)
    time.sleep(20)
    driver.find_element_by_xpath("//select[@data-type='orderby'][@class='select_sort']//option[@value='1']").click()

    print("comment_url:"+comment_url)

    file = open("Item/Qunar/comments/"+ht[3]+".txt", 'a', encoding='utf-8')
    for p in range(1, int(int(ccount)/15)):                    #每页获取评论
        quits = 0                        # 是否跳出本次循环
        if p < int(int(ccount)/15):
            time.sleep(15)                                      # 休眠30s
            # driver.execute_script("document.body.scrollTop=document.body.scrollHeight")
            source = driver.page_source
            selector = etree.HTML(source)
            content = selector.xpath("//div[@class='J_commentDetail']/text()")
            date = selector.xpath("//span[@class='date']/text()")       #入住时间
            print(date)
            for i in range(len(content)):
                print(content[i])
                print(date[i])
                setting_date = date[i]
                temp = setting_date.split("年")
                Y = temp[0]
                m = temp[1].split("月")[0]

                setting_date_ts = time.mktime(time.strptime(Y+m, "%Y%m"))           # 入住时间的时间戳
                if setting_date_ts > time.mktime(time.strptime("201612", "%Y%m")):  # 在201612月后入住的评论信息
                    file.write(content[i])
                    file.write("\r\n")
                    file.write("\r\n")
                else:
                    quits = 1

                # sql = "INSERT INTO `comments`(`content`, `date`, `ht_id`, `page_num`) VALUES('%s', '%s', '%d', '%d')"
                # data = (str(content[i]).strip("\\x"), str(date[i]), ht_id, p)
                # cursor.execute(sql%data)
                # conn.commit()

            #

            try:
                # xpath = "//div[@class='c_page_list layoutfix']//a[@value=" + str(p + 1) + "]"
                # driver.find_element_by_xpath(xpath=xpath).click()
                page_num = "//div[@class='c_pagevalue']/input[@id='cPageNum']"
                submit = "//div[@class='c_pagevalue']//input[@id='cPageBtn']"
                print("current page:"+str(p+1))

                driver.find_element_by_xpath(xpath=page_num).clear()
                driver.find_element_by_xpath(xpath=page_num).send_keys(str(p + 1))
                time.sleep(5)
                driver.find_element_by_xpath(xpath=submit).click()
            except NoSuchElementException as e:
                # xpath = "//div[@class='c_page']//a[@class='c_down']"
                # driver.find_element_by_xpath(xpath=xpath).click()
                # raise
                continue
        if quits == 1:
            break       #跳出本家酒店的评论信息抓取
    file.close()
    driver.close()


cursor.close()
conn.close()