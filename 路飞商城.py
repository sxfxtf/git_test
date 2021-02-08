#!/user/bin/env python
# -*- coding:UTF-8 -*-
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
import time
from lxml import etree
import os

login_url = 'https://www.luffycity.com/study/degree'
br = webdriver.Chrome()
br.get(url=login_url)
br.find_element_by_xpath("//div[@class='username inputcontain']/input").send_keys("15867416745")
br.find_element_by_xpath("//div[@class='password inputcontain']/input").send_keys("192406")
# br.find_element_by_xpath("//div[@class='signin']/input").send_keys("192406")
t = " "
end_str = "1.55 socketserver源码解析2"
while 1:
    print("进入第一个循环")
    flag = 0
    try:
        br.find_element_by_class_name("media-player")
    except Exception:
        print("播放界面没找到,等待5秒")
        time.sleep(5)
    else:
        time.sleep(2)
        print("找到课程播放框,开始监控......")
        page = br.page_source
        tree = etree.HTML(page)

        if t == end_str:
            br.quit()
            os.system("shutdown -s -t 5")
            os.system("taskkill -im pycharm64.exe")
            # exit("程序退出了")
        else:
            print("不是 %s, 继续运行"%end_str)

        titile = tree.xpath("//div[@class='section active']/section[1]/h5/text()")
        play_time = tree.xpath("//div[@class='section active']/section[2]/span/text()")
        print(play_time)
        print("%s 视频,一共播放时长为 %s" % (titile[0], play_time[0]))
        t = titile[0]
        wait_time = play_time[0].split(":")[0]
        flag = 1
        print("等待时间为%s分钟" % wait_time)
        time.sleep(int(wait_time)*60)
        # time.sleep(5)
        while flag:
            print("内部循环开始")
            try:
                br.find_element_by_xpath("//img[@alt='关闭按钮']").click()
                time.sleep(1)
                br.find_element_by_xpath("//button[@class='next-button']").click()
                flag = 0
                # break
            except exceptions.NoSuchElementException:
                print("找不到调查窗口点击下一章节")
                try:
                    br.find_element_by_xpath("//button[@class='next-button']").click()
                    flag = 0
                except Exception:
                    time.sleep(3)
                    print("未找到调查弹窗,等待3秒")
            except exceptions.WebDriverException:
                br.quit()
            # except Exception:
            #     time.sleep(3)
            #     print("未找到调查弹窗,等待3秒")



            # try:
            #     br.find_element_by_xpath("//img[@alt='关闭按钮']").click()
            #     time.sleep(1)
            #     br.find_element_by_xpath("//button[@class='next-button']").click()
            #     flag = 0
            #     break
            # except exceptions.NoSuchAttributeException:
            #     br.find_element_by_xpath("//button[@class='next-button']").click()
            #     flag = 0
            #     break
            # except Exception:
            #     time.sleep(3)
            #     print("未找到调查弹窗,等待3秒")
